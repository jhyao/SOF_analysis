import asyncio

from data.models.sof_models import User
from data.config.config import Config
from data.spider.sof_spider import UsersApi

import unittest
import logging

config = Config('test')

class TestUserModel(unittest.TestCase):
    def test_insert(self):
        async def inner():
            User.raw("truncate table user;").execute()
            data = await UsersApi().get_async()
            for item in data:
                print(item)
                await User.execute_query(User.insert(item))
            User.raw("truncate table user;").execute()
        asyncio.get_event_loop().run_until_complete(inner())
