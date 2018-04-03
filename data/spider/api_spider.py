import aiohttp
from .constants import *
import asyncio
import requests
from . import config
import logging

logger = logging.getLogger(__name__)

class ApiSpider(object):
    session = None
    session_async = None

    all_params = config.all_params_default
    required = config.required_default
    api_url = config.api_url
    url_pattern = ''

    def __init__(self, **kwargs):
        self.params = self.fix_params(kwargs)
    
    @classmethod
    def fix_params(cls, params):
        # delete invaild params
        params = dict(params)
        if cls.all_params:
            for key in list(params.keys()):
                if key not in cls.all_params:
                    params.pop(key)
        # set default value for required params, or throw exception if have no default in all_params
        for key in cls.required:
            if key not in params:
                if cls.all_params.get(key, None) is None:
                    raise Exception('param ' + key + ' is required')
                else:
                    params.setdefault(key, cls.all_params.get(key))
        return params
    
    @classmethod
    def get_url(cls, url_pattern, ids=None):
        '''
        Params url_pattern: python string format, url_pattern.format(ids=ids)
        Example:
            cls.get_url('users/{ids}/answers', ids='123;12312')
            return '.....'/users/123;12312/answers
        '''
        url = cls.api_url
        if not url_pattern:
            return url
        
        try:
            path = url_pattern.format(ids=cls.format_ids(ids))
        except KeyError as e:
            raise Exception('url pattern need param ' + e.args)
        
        if cls.api_url[-1] == '/':
            url += path
        else:
            url += '/' + path
        return url
    
    @staticmethod
    def format_ids(ids):
        '''
        format ids like '123;12312;234324'
        accept input: list of str, list of int, str aplit with ';', single int id
        '''
        if not ids:
            return ''
        if isinstance(ids, list) and len(ids) > 0:
            return ';'.join([str(item) for item in ids])
        elif isinstance(ids, str):
            return ';'.join([item.strip() for item in ids.split(';')])
        elif isinstance(ids, int):
            return str(ids)
        else:
            raise Exception('wrong ids format')
    
    @staticmethod
    def page_add(params):
        if Param.PAGE not in params:
            params[Param.PAGE] = 2
        else:
            params[Param.PAGE] += 1
    
    def update_params(self, **kwargs):
        self.params.update(**kwargs)
        self.fix_params(self.params)

    def get(self, ids=None, **kwargs):
        '''
        get one page data, use params set in constructor, can change them temporarily through kwargs
        '''
        url = self.get_url(self.url_pattern, ids)
        params = dict(self.params)
        params.update(kwargs)
        params = self.fix_params(params)
        if not self.session:
            self.session = requests.Session()
        with self.session.get(url, params=params) as resp:
            logger.info('GET ' + resp.url)
            data = resp.json()
            return data.get(RespKey.ITEMS, [])

    def get_pages(self, ids=None, max_pages=0, **kwargs):
        '''
        generator for get data of pages
        max_pages: default 0 to get all pages
        '''
        url = self.get_url(self.url_pattern, ids)
        params = dict(self.params)
        params.update(kwargs)
        params = self.fix_params(params)
        if not self.session:
            self.session = requests.Session()
        page = 0
        max_pages = 0 if max_pages < 0 else max_pages   
        data = {}  
        while (page==0 or data.get(RespKey.HAS_MORE, False)) and (max_pages == 0 or page < max_pages):
            self.page_add(params)
            with self.session.get(url, params=params) as resp:
                logger.info('GET ' + resp.url)
                data = resp.json()
                page += 1
                yield data.get(RespKey.ITEMS, [])
    
    def __del__(self):
        try:
            self.session.close()
        finally:
            self.session = None


class UserApider(ApiSpider):
    url_pattern = 'users'

    def get