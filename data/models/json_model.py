from peewee import Model
import json


class JSONModel(Model):

    @classmethod
    def load_data(cls, data_json):
        data = json.loads(data_json, encoding='utf-8')
        return data

    @classmethod
    def make_from_json(cls, data_json):
        data = cls.load_data(data_json)
        return cls(**data)
    
    @classmethod
    def create_from_json(cls, create_json):
        create = cls.load_data(create_json)
        return cls.create(**create)
    
    @classmethod
    def update_from_json(cls, update_json):
        update = cls.load_data(update_json)
        return cls.update(**data)
    
    @classmethod
    def insert_from_json(cls, insert_json):
        insert = cls.load_data(insert_json)
        return cls.insert(insert)
    
    @classmethod
    def insert_many_from_json(cls, rows_json, fields=None):
        rows = cls.load_data(rows_json)
        return cls.insert_many(rows, fields)
    
    @classmethod
    def replace_from_json(cls, insert_json):
        insert = cls.load_data(insert_json)
        return cls.replace(insert)
    
    @classmethod
    def replace_many_from_json(cls, rows_json, fields=None):
        rows = cls.load_data(rows_json)
        return cls.replace_many(rows, fields)

    def get_json(self):
        return json.dumps(self.__data__)

    def __str__(self):
        return self.get_json()