import ast
import json

from data.config.config import config
from redis import StrictRedis


class Cache:
    redis = StrictRedis(connection_pool=config.redis)
    key = None
    isjson = False

    @classmethod
    def get(cls, default=None):
        return cls.transfer_data(cls.redis.get(cls.key), default=default)

    @classmethod
    def set(cls, value, **kwargs):
        if cls.isjson:
            value = json.dumps(value)
        return cls.redis.set(cls.key, value, **kwargs)

    @classmethod
    def hset(cls, name, value):
        if cls.isjson:
            value = json.dumps(value)
        return cls.redis.hset(cls.key, name, value)

    @classmethod
    def hget(cls, name, default=None):
        return cls.transfer_data(cls.redis.hget(cls.key, name), default=default)

    @classmethod
    def hmset(cls, data):
        if cls.isjson:
            data = dict([(key, json.dumps(data[key])) for key in data])
        return cls.redis.hmset(cls.key, data)

    @classmethod
    def hmget(cls, names, default=None):
        return cls.transfer_data(cls.redis.hmget(cls.key, names), default=default)

    @classmethod
    def hgetall(cls, default=None):
        return cls.transfer_data(cls.redis.hgetall(cls.key), default=default)

    @classmethod
    def clear(cls):
        if cls.redis.exists(cls.key):
            return cls.redis.delete(cls.key)

    @classmethod
    def transfer_data(cls, data, default=None):
        if not data:
            return default
        elif isinstance(data, str):
            return cls.transfer_item(data)
        elif isinstance(data, dict):
            return dict([(key, cls.transfer_item(data[key])) for key in data])
        else:
            return data

    @classmethod
    def transfer_item(cls, item):
        if cls.isjson:
            return json.loads(item)
        else:
            try:
                return ast.literal_eval(item)
            except:
                return item

    @classmethod
    def hdel(cls, name):
        cls.redis.hdel(cls.key, name)