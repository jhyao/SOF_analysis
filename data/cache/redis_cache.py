import ast
import json

from data.config.config import config
from redis import StrictRedis


class Cache:
    redis = StrictRedis(connection_pool=config.redis)
    key = None

    @classmethod
    def get(cls, default=None, isjson=False):
        return cls.transfer_data(cls.redis.get(cls.key), default=default, isjson=isjson)

    @classmethod
    def set(cls, value, to_json=False, **kwargs):
        if to_json:
            value = json.dumps(value)
        return cls.redis.set(cls.key, value, **kwargs)

    @classmethod
    def hset(cls, name, value, to_json=False):
        if to_json:
            value = json.dumps(value)
        return cls.redis.hset(cls.key, name, value)

    @classmethod
    def hget(cls, name, default=None, isjson=False):
        return cls.transfer_data(cls.redis.hget(cls.key, name), default=default, isjson=isjson)

    @classmethod
    def hmset(cls, data, to_json=False):
        if to_json:
            data = dict([(key, json.dumps(data[key])) for key in data])
        return cls.redis.hmset(cls.key, data)

    @classmethod
    def hmget(cls, names, default=None, isjson=False):
        return cls.transfer_data(cls.redis.hmget(cls.key, names), default=default, isjson=isjson)

    @classmethod
    def hgetall(cls, default=None, isjson=False):
        return cls.transfer_data(cls.redis.hgetall(cls.key), default=default, isjson=isjson)

    @classmethod
    def clear(cls):
        if cls.redis.exists(cls.key):
            return cls.redis.delete(cls.key)

    @classmethod
    def transfer_data(cls, data, default=None, isjson=False):
        if not data:
            return default
        elif isinstance(data, str):
            return cls.transfer_item(data, isjson=isjson)
        elif isinstance(data, dict):
            return dict([(key, cls.transfer_item(data[key], isjson=isjson)) for key in data])
        else:
            return data

    @classmethod
    def transfer_item(cls, item, isjson=False):
        if isjson:
            return json.loads(item)
        else:
            try:
                return ast.literal_eval(item)
            except:
                return item
