import aiohttp
from .constants import *
import asyncio
import requests
from . import config
import logging
from .api_error import *

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
                    raise ParamsError('param ' + key + ' is required')
                else:
                    params.setdefault(key, cls.all_params.get(key))
        return params
    
    @classmethod
    def get_url(cls, url_pattern, keys=None):
        '''
        Params url_pattern: python string format, url_pattern.format(keys=keys)
        Example:
            cls.get_url('users/{keys}/answers', keys='123;12312')
            return '.....'/users/123;12312/answers
        '''
        url = cls.api_url
        if not url_pattern:
            return url
        
        try:
            if keys:
                path = url_pattern.format(keys=cls.format_keys(keys))
            else:
                path = url_pattern.format()
        except KeyError:
            raise KeysError('url pattern need keys')
        
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
    
    def update_params(self, **kwargs):
        self.params.update(**kwargs)
        self.fix_params(self.params)

    def get(self, keys=None, **kwargs):
        '''
        get one page data, use params set in constructor, can change them temporarily through kwargs
        '''
        url = self.get_url(self.url_pattern, keys)
        params = dict(self.params)
        params.update(kwargs)
        params = self.fix_params(params)
        if not self.session:
            self.session = requests.Session()
        with self.session.get(url, params=params) as resp:
            logger.info('GET ' + resp.url)
            data = resp.json()
            return self.data_transfer(data)

    def get_pages(self, keys=None, max_pages=0, **kwargs):
        '''
        generator for get data of pages
        max_pages: default 0 to get all pages
        '''
        url = self.get_url(self.url_pattern, keys)
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
                yield self.data_transfer(data)
    
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
    
    def __del__(self):
        try:
            if self.session:
                self.session.close()
        finally:
            self.session = None
