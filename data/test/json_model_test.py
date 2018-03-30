import unittest
from peewee import *
from ..models.json_model import JSONModel
from ..config import config
import datetime
import json

class Test(JSONModel):
    class Meta:
        database = config.database
    
    id = IntegerField(primary_key=True)
    name = CharField()
    date = TimestampField(utc=True, null=True)

class TestJSONModel(unittest.TestCase):
    
    db = config.database

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
    
    def test_make(self):
        obj = Test.make(id=3, name='name', date=datetime.datetime(2018, 3, 29))
        self.assertDictEqual({'id':3, 'name':'name', 'date':datetime.datetime(2018, 3, 29)}, obj.get_data())
    
    def test_make_from_json(self):
        obj = Test.make_from_json('{"id": 3, "name": "yjh", "date": 1522260330}')
        self.assertDictEqual({'id':3, 'name':'yjh', 'date': 1522260330}, obj.get_data())
    
    def test_create(self):
        obj = Test.create(id="3", name="yjh", date=1522260330)
        self.assertDictEqual({'id':'3', 'name':'yjh', 'date': 1522260330}, obj.get_data())
    
    def test_create_from_json(self):
        obj = Test.create_from_json('{"id": "3", "name": "yjh", "date": 1522260330}')
        self.assertDictEqual({'id':'3', 'name':'yjh', 'date': 1522260330}, obj.get_data())
    
    def test_create_from_json_chinese(self):
        obj = Test.create_from_json('{"id": "3", "name": "张三", "date": 1522260330}')
        self.assertDictEqual({'id':'3', 'name':'张三', 'date': 1522260330}, obj.get_data())
    
    def test_update(self):
        Test.update(name='asd').where(id==2).execute()
        obj = Test.get(id=2)
        self.assertEqual('asd', obj.name)
    
    def test_update_from_json(self):
        Test.update_from_json('{"name": "asd"}').where(id==2).execute()
        obj = Test.get(id=2)
        self.assertEqual('asd', obj.name)
    
    def test_insert(self):
        num = Test.insert(id=3, name='test3').execute()
        # return None
        # self.assertEqual(1, num) 
        obj = Test.get(id=3)
        self.assertEqual('test3', obj.name)
    
    def test_insert_from_json(self):
        num = Test.insert_from_json('{"id":"3", "name":"test3"}').execute()
        # return None
        # self.assertEqual(1, num)
        obj = Test.get(id=3)
        self.assertEqual('test3', obj.name)
    
    def test_insert_many(self):
        num = Test.insert_many([{'id':3, 'name':'test3'},{'id':4, 'name':'test4'},{'id':5, 'name':'test5'}]).execute()
        # return True
        # self.assertEqual(3, num)
        for item in Test.select().where(Test.id >= 3):
            self.assertEqual('test'+str(item.id), item.name)
    
    def test_insert_many_from_json(self):
        num = Test.insert_many_from_json('[{"id":"3","name":"test3"},{"id":"4","name":"test4"},{"id":"5","name":"test5"}]').execute()
        # return True
        # self.assertEqual(3, num)
        for item in Test.select().where(Test.id >= 3):
            self.assertEqual('test'+str(item.id), item.name)
    
    def test_get_select_single(self):
        select = Test.select()
        obj = Test.get_select(select, single=True)
        self.assertEqual('test1', obj.name)
    
    def test_get_select_single_none(self):
        select = Test.select().where(Test.id >= 3)
        self.assertRaises(Test.DoesNotExist, Test.get_select, select, single=True)
    
    def test_get_select_all(self):
        select = Test.select()
        objlist = Test.get_select(select)
        self.assertEqual(2, len(objlist))
        self.assertEqual('test1', objlist[0].name)
        self.assertEqual('test2', objlist[1].name)
    
    def test_get_select_all_none(self):
        select = Test.select().where(Test.id >= 3)
        objlist = Test.get_select(select)
        self.assertEqual(0, len(objlist))
    
    def test_get_select_single_to_json(self):
        select = Test.select()
        obj_json = Test.get_select_to_json(select, single=True)
        obj = json.loads(obj_json, encoding='utf-8')
        self.assertEqual('test1', obj.get('name'))
    
    def test_get_select_all_to_json(self):
        select = Test.select()
        obj_json = Test.get_select_to_json(select)
        obj = json.loads(obj_json, encoding='utf-8')
        self.assertEqual('test1', obj[0].get('name'))
        self.assertEqual('test2', obj[1].get('name'))
    
    def test_dump_json(self):
        obj = Test.make(id=4, name='张三', date=datetime.datetime(2018, 3, 29))
        obj_json = Test.dump_json(obj)
        load = json.loads(obj_json, encoding='utf-8')
        self.assertEqual('张三', load.get('name'))
        self.assertEqual(1522252800, load.get('date'))
    
    def test_get_all(self):
        objlist = Test.get_all()
        self.assertEqual(2, len(objlist))
        self.assertEqual('test1', objlist[0].name)
        self.assertEqual('test2', objlist[1].name)
    
    def test_get_all_none(self):
        objlist = Test.get_all(Test.id > 3)
        self.assertEqual(0, len(objlist))
    
    def test_get_all_to_json(self):
        obj_json = Test.get_all_to_json()
        objlist = json.loads(obj_json)
        self.assertEqual(2, len(objlist))
        self.assertEqual('test1', objlist[0].get('name'))
        self.assertEqual('test2', objlist[1].get('name'))

if __name__ == '__main__':
    unittest.main()