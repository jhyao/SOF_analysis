import unittest
from ..spider.api_spider import ApiSpider, UserApider
import itertools

class TestApiSpider(unittest.TestCase):
    def test_get(self):
        data = UserApider(pagesize=10).get()
        self.assertEqual(10, len(data))
    
    def test_get_change_params(self):
        data = UserApider(pagesize=10).get(pagesize=5)
        self.assertEqual(5, len(data))
    
    def test_get_pages(self):
        pages = UserApider(pagesize=10).get_pages(max_pages=5)
        data = []
        i = 0
        for page in pages:
            self.assertEqual(10, len(page))
            i += 1
        self.assertEqual(5, i)

if __name__ == '__main__':
    unittest.main()