import asyncio
import datetime
import json
import unittest

import peewee_async
from peewee import *

from ..config import models_config as config
from ..models.json_model_async import JSONModel_async


class Test(JSONModel_async):
    class Meta:
        database = config.database_async
    
    manager = peewee_async.Manager(config.database_async)
    
    id = IntegerField(primary_key=True)
    name = CharField()
    date = TimestampField(utc=True, null=True)

class TestJSONModel(unittest.TestCase):
    
    db = config.database_async
    loop = asyncio.get_event_loop()

    @classmethod
    def setUpClass(cls):
        cls.db.connect()
        cls.db.create_tables([Test])
    
    @classmethod
    def tearDownClass(cls):
        cls.db.drop_tables([Test])
        cls.db.close()
    
    def setUp(self):
        Test.raw("insert into test values(1, 'test1', 1522166400), (2, 'test2', 1522080000);").execute()
    
    def tearDown(self):
        Test.raw("truncate table test;").execute()
    
    def test_create(self):
        async def inner():
            obj = await Test.create(id="3", name="yjh", date=1522260330)
            self.assertEqual({'id':'3', 'name':'yjh', 'date': 1522260330}, obj.get_data())
        self.loop.run_until_complete(inner())
    
    def test_create_from_json(self):
        async def inner():
            obj = await Test.create_from_json('{"id": "3", "name": "yjh", "date": 1522260330}')
            self.assertEqual({'id':'3', 'name':'yjh', 'date': 1522260330}, obj.get_data())
        self.loop.run_until_complete(inner())
    
    def test_create_from_json_chinese(self):
        async def inner():
            obj = await Test.create_from_json('{"id": "3", "name": "张三", "date": 1522260330}')
            self.assertDictEqual({'id':'3', 'name':'张三', 'date': 1522260330}, obj.get_data())
        self.loop.run_until_complete(inner())
    
    def test_update(self):
        async def inner():
            await Test.execute_query(Test.update(name='asd').where(id==2))
            obj = await Test.get(id=2)
            self.assertEqual('asd', obj.name)
        self.loop.run_until_complete(inner())
    
    def test_insert(self):
        async def inner():
            await Test.execute_query(Test.insert(id=3, name='test3'))
            obj = await Test.get(id=3)
            self.assertEqual('test3', obj.name)
        self.loop.run_until_complete(inner())
    
    def test_get_select_single(self):
        async def inner():
            select = Test.select()
            obj = await Test.get_select(select, single=True)
            self.assertEqual('test1', obj.name)
        self.loop.run_until_complete(inner())
    
    def test_get_select_single_none(self):
        async def inner():
            select = Test.select().where(Test.id > 3)
            obj = await Test.get_select(select, single=True)
        self.assertRaises(Test.DoesNotExist, self.loop.run_until_complete, inner())
    
    def test_get_select_all(self):
        async def inner():
            select = Test.select()
            objlist = await Test.get_select(select)
            self.assertEqual(2, len(objlist))
            self.assertEqual('test1', objlist[0].name)
            self.assertEqual('test2', objlist[1].name)
        self.loop.run_until_complete(inner())
    
    def test_get_select_all_none(self):
        async def inner():
            select = Test.select().where(Test.id > 3)
            objlist = await Test.get_select(select)
            self.assertEqual(0, len(objlist))
        self.loop.run_until_complete(inner())
    
    def test_get_select_single_to_json(self):
        async def inner():
            select = Test.select()
            obj_json = await Test.get_select_to_json(select, single=True)
            obj = json.loads(obj_json, encoding='utf-8')
            self.assertEqual('test1', obj.get('name'))
        self.loop.run_until_complete(inner())
    
    def test_get_select_to_json(self):
        async def inner():
            select = Test.select()
            obj_json = await Test.get_select_to_json(select)
            obj = json.loads(obj_json, encoding='utf-8')
            self.assertEqual('test1', obj[0].get('name'))
            self.assertEqual('test2', obj[1].get('name'))
        self.loop.run_until_complete(inner())
    
    def test_get(self):
        async def inner():
            obj = await Test.get(id=1)
            self.assertEqual('test1', obj.name)
        self.loop.run_until_complete(inner())
    
    def test_get_none(self):
        async def inner():
            obj = await Test.get(id=3)
            self.assertEqual('test1', obj.name)
        self.assertRaises(Test.DoesNotExist, self.loop.run_until_complete, inner())
    
    def test_get_all(self):
        async def inner():
            objlist = await Test.get_all(Test.id > 0)
            self.assertEqual(2, len(objlist))
        self.loop.run_until_complete(inner())
    
    def test_get_all_none(self):
        async def inner():
            objlist = await Test.get_all(Test.id > 3)
            self.assertEqual(0, len(objlist))
        self.loop.run_until_complete(inner())
    
    def test_get_to_json(self):
        async def inner():
            obj_json = await Test.get_to_json(id=1)
            obj = json.loads(obj_json, encoding='utf-8')
            self.assertEqual('test1', obj.get('name'))
        self.loop.run_until_complete(inner())
    
    def test_get_all_to_json(self):
        async def inner():
            obj_json = await Test.get_all_to_json(Test.id > 0)
            objlist = json.loads(obj_json, encoding='utf-8')
            self.assertEqual(2, len(objlist))
            self.assertEqual('test1', objlist[0].get('name'))
            self.assertEqual('test2', objlist[1].get('name'))
        self.loop.run_until_complete(inner())
    
    def test_save_create(self):
        async def inner():
            obj = Test.make(id=3, name='test3')
            await obj.save(force_insert=True)
            obj_new = await Test.get(id=3)
            self.assertEqual('test3', obj_new.name)
        self.loop.run_until_complete(inner())
    
    def test_save_update(self):
        async def inner():
            obj = await Test.get(id=2)
            obj.name = 'test2_new'
            await obj.save()
            obj_new = await Test.get(id=2)
            self.assertEqual('test2_new', obj_new.name)
        self.loop.run_until_complete(inner())

if __name__ == '__main__':
    unittest.main()
