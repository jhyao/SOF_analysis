import asyncio
from asyncio import Lock

import time

from .cdn_error import PageEnd
from ..models.json_model_async import JSONModel_async
from ..spider.api_spider import ApiSpider, DataError, BackOffError
from ..cache.redis_cache import Cache
import logging

logger = logging.getLogger(__name__)


class CDN(object):
    model = JSONModel_async
    api = ApiSpider
    cache = Cache

    @classmethod
    def get_cache(cls, key):
        return cls.cache.get(key)

    @classmethod
    def set_cache(cls, key, value, **kwargs):
        return cls.cache.set(key, value, **kwargs)

    @classmethod
    def count(cls, unit=10000, **kwargs):
        spider = cls.api(**kwargs)
        page_size = spider.params.get('pagesize', None)
        if page_size is None:
            spider.update_params(pagesize=100)
        page_size = spider.params.get('pagesize')
        unit = unit // page_size
        start = 0
        end = unit
        data = spider.get(page=end)
        # determine end if the prediction given is too small
        while len(data) == page_size:
            start = end
            end += unit
            data = spider.get(page=end)
        # find the last page with division
        middle = (start + end) // 2
        while start != end:
            middle = (start + end) // 2
            data = spider.get(page=middle)
            if len(data) == 0:
                end = middle - 1
            elif len(data) == page_size:
                start = middle + 1
        else:
            data = spider.get(page=start)
        return page_size * (start - 1) + len(data)

    @classmethod
    def dld_page(cls, save=True, **kwargs):
        page_data = cls.api(**kwargs).get()
        if save:
            cls.model.insert_many_execute(page_data)

    @classmethod
    async def dld_page_async(cls, save=True, **kwargs):
        page_data = await cls.api(**kwargs).get_async()
        if save:
            await cls.model.insert_many_execute_async(page_data)
        return len(page_data)

    class Pager:
        def __init__(self, page, max_page=None):
            self.page = page
            self.max_page = max_page
            self.lock = Lock()
            if max_page is not None and page > max_page:
                raise PageEnd()
            self.__back_off_occur = None
            self.__back__off_time = None

        async def get_page(self):
            if self.max_page is not None and self.page > self.max_page:
                raise PageEnd()
            if self.__back_off_occur and self.__back__off_time:
                sleep_time = self.__back__off_time - time.time() + self.__back_off_occur
                if sleep_time > 0:
                    await asyncio.sleep(sleep_time + 0.5)
            async with self.lock:
                result = self.page
                self.page += 1
                return result

        def back_off(self, bo_time):
            self.__back_off_occur = time.time()
            self.__back__off_time = bo_time

    @classmethod
    async def dld_pages_async(cls, pager_async=None, save=True, **kwargs):
        if pager_async is None:
            pager_async = cls.Pager(kwargs.pop('page', 1), kwargs.pop('max_page', None))
        fail_pages = []
        while True:
            try:
                page = await pager_async.get_page()
            except PageEnd:
                break
            try:
                size = await cls.dld_page_async(page=page, save=save, **kwargs)
                if size == 0:
                    break
            except BackOffError as backoff:
                bo_time = backoff.args[0]
                logger.warning(f'backoff {bo_time} occur on page {page}')
                # pager_async.back_off(bo_time)
                time.sleep(bo_time)
            except Exception as e:
                logger.error(e.__class__.__name__ + str(e.args))
                fail_pages.append(page)
                break
        if fail_pages:
            logger.error('dld pages failed: ' + str(fail_pages))

    @classmethod
    async def dld_pages_async_parallel(cls, parallel_num=5, save=True, **kwargs):
        pager = cls.Pager(kwargs.pop('page', 1), kwargs.pop('max_page', None))
        task_list = [cls.dld_pages_async(pager, save=save, **kwargs) for i in range(parallel_num)]
        await asyncio.wait(task_list)








