import unittest
from ..spider.sof_spider import *
import itertools
from ..spider.api_error import *

class TestApiSpider(unittest.TestCase):
    def test_get(self):
        data = UsersApi(pagesize=10).get()
        self.assertEqual(10, len(data))
    
    def test_get_change_params(self):
        data = UsersApi(pagesize=10).get(pagesize=5)
        self.assertEqual(5, len(data))
    
    def test_get_pages(self):
        pages = UsersApi(pagesize=10).get_pages(max_pages=5)
        data = []
        i = 0
        for page in pages:
            self.assertEqual(10, len(page))
            i += 1
        self.assertEqual(5, i)
    
    def test_get_transfer(self):
        data = UsersApi(pagesize=1).get()
        self.assertEqual(1, len(data))
        user = data[0]
        self.assertTrue('badge_gold' in user)
    
    def test_get_user_ids(self):
        data = UsersByIdsApi(pagesize=10).get(user_ids=[123])
        self.assertEqual(1, len(data))
        user = data[0]
        self.assertEqual(123, user['user_id'])
    
    def test_get_user_ids_no_ids(self):
        self.assertRaises(UrlKeysError, UsersByIdsApi(pagesize=10).get)
    
    def test_get_user_ids_wrong_ids(self):
        self.assertRaises(DataError, UsersByIdsApi(pagesize=10).get, user_ids='sdfsdf')
    


if __name__ == '__main__':
    unittest.main()