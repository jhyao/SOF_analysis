import asyncio
import logging

import aiohttp
import requests

from ..config import spider_config
from .api_error import *
from ..config.spider_constants import *

logger = logging.getLogger(__name__)


class ApiSpider(object):
    
    config = spider_config.DefaultConfig

    api_url = spider_config.api_url

    def __init__(self, **kwargs):
        self.params = self.fix_params(kwargs)
    
    @classmethod
    def fix_params(cls, params):
        # delete invaild params
        params = dict(params)
        for key in set(params.keys()) - set(cls.config.all_params.keys()):
            params.pop(key)
        for key in set(cls.config.all_params.keys()) - set(params.keys()):
            if cls.config.all_params.get(key) is not None:
                params[key] = cls.config.all_params.get(key)
        for key in cls.config.required:
            if params.get(key, None) is None:
                raise UrlParamsError('param ' + key + ' is required')
        return params
    
    @classmethod
    def get_url(cls, url_pattern, keys):
        '''
        Params url_pattern: python string format, url_pattern.format(keys=keys)
        Example:
            cls.get_url('users/{keys}/answers', keys='123;12312')
            return '.....'/users/123;12312/answers
        '''
        url = cls.api_url
        if not url_pattern:
            return url

        for key in list(keys.keys()):
            foramt_key = cls.format_keys(keys[key])
            if foramt_key:
                keys[key] = foramt_key
            else:
                keys.pop(key)

        try:
            if keys:
                path = url_pattern.format(**keys)
            else:
                path = url_pattern.format()
        except KeyError:
            raise UrlKeysError('url pattern ' + url_pattern + ' need keys')
        
        if cls.api_url[-1] == '/':
            url += path
        else:
            url += '/' + path
        return url
    
    @staticmethod
    def format_keys(keys):
        '''
        format keys like '123;12312;234324'
        accept input: list of str, list of int, str aplit with ';', single int id
        '''
        if not keys:
            return None
        if isinstance(keys, list) and len(keys) > 0:
            return ';'.join([str(item) for item in keys])
        elif isinstance(keys, str):
            return ';'.join([item.strip() for item in keys.split(';')])
        elif isinstance(keys, int):
            return str(keys)
        else:
            raise KeysError('wrong keys format')
    
    @staticmethod
    def page_add(params):
        if Param.PAGE not in params:
            params[Param.PAGE] = 2
        else:
            params[Param.PAGE] += 1
    
    def __url_and_params(self, **kwargs):
        keys = {}
        try:
            for key in self.config.keys_required:
                keys[key] = kwargs.pop(key)
        except KeyError:
            raise UrlKeysError('url pattern ' + self.config.url_pattern + ' need keys')
        url = self.get_url(self.config.url_pattern, keys)
        params = dict(self.params)
        params.update(kwargs)
        params = self.fix_params(params)
        return url, params
    
    def update_params(self, **kwargs):
        self.params.update(**kwargs)
        self.fix_params(self.params)

    def get(self, **kwargs):
        '''
        get one page data, use params set in constructor, can change them temporarily through kwargs
        '''
        (url, params) = self.__url_and_params(**kwargs)
        with requests.Session() as session:
            with session.get(url, params=params) as resp:
                logger.info('GET ' + str(resp.url))
                data = resp.json()
                return self.data_transfer(data)
    
    async def get_async(self, **kwargs):
        '''
        get one page data, use params set in constructor, can change them temporarily through kwargs
        '''
        (url, params) = self.__url_and_params(**kwargs)
        async with aiohttp.ClientSession() as session:
            async with session.get(url, params=params) as resp:
                logger.info('GET ' + str(resp.url))
                data = await resp.json()
                return self.data_transfer(data)

    def get_pages(self, keys=None, max_pages=0, **kwargs):
        '''
        generator for get data of pages
        max_pages: default 0 to get all pages
        '''
        (url, params) = self.__url_and_params(**kwargs)
        page = 0
        max_pages = 0 if max_pages < 0 else max_pages
        data = {}
        with requests.Session() as session:
            while (page==0 or data.get(RespKey.HAS_MORE, False)) and (max_pages == 0 or page < max_pages):
                with session.get(url, params=params) as resp:
                    logger.info('GET ' + str(resp.url))
                    data = resp.json()
                    yield self.data_transfer(data)
                page += 1
                self.page_add(params)
    
    async def get_pages_async(self, keys=None, max_pages=0, **kwargs):
        '''
        generator for get data of pages
        max_pages: default 0 to get all pages
        '''
        (url, params) = self.__url_and_params(**kwargs)
        page = 0
        max_pages = 0 if max_pages < 0 else max_pages
        data = {}
        with aiohttp.ClientSession() as session:
            while (page==0 or data.get(RespKey.HAS_MORE, False)) and (max_pages == 0 or page < max_pages):
                async with session.get(url, params=params) as resp:
                    logger.info(f'GET {resp.url}')
                    data = await resp.json()
                    yield self.data_transfer(data)
                page += 1
                self.page_add(params)
    
    def data_transfer(self, data):
        '''
        overwrite this method to handle data
        '''
        if 'error_id' in data:
            raise DataError('ERROR{error_id}: {error_name}({error_message})'.format(**data))
        results = data.get(RespKey.ITEMS, [])
        for item in results:
            self.item_transfer(item)
        return results
    
    def item_transfer(self, item):
        '''
        overwrite this method to handle item
        '''
        pass
