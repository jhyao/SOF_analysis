import unittest
from data.cache.redis_cache import Cache
class CacheTest(unittest.TestCase):

    def setUp(self):
        Cache.key = 'test'
        Cache.clear()

    def tearDown(self):
        Cache.clear()
