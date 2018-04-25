
from data.config.config import config
from redis import StrictRedis


class Cache:
    redis = StrictRedis(connection_pool=config.redis)

    @classmethod
    def get(cls, key):
        return cls.redis.get(key)

    @classmethod
    def set(cls, key, value, **kwargs):
        return cls.redis.set(key, value, **kwargs)
