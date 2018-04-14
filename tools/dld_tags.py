import asyncio
import time

from data.models.sof_models import *
from data.spider.sof_spider import *
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

page_from = 314


def get_page():
    global page_from
    page_from += 1
    return page_from

async def dld_tags():
    fail_page = []
    while True:
        page = get_page()
        try:
            page_data = await TagsApi(page=page, pagesize=100).get_async()
            await Tag.insert_many_execute_async(page_data)
            if len(page_data) == 0:
                break
        except Exception as e:
            logger.error(e.__class__.__name__ + str(e.args))
            fail_page.append(page)
    with open('dld_tags_log.log', 'w') as f:
        f.writelines(str(fail_page))


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(asyncio.gather(dld_tags(), dld_tags(), dld_tags(), dld_tags(), dld_tags()))
    loop.close()


