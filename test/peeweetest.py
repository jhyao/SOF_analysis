from peewee import *
import json

db = MySQLDatabase("sof_basic", host="localhost", user='root', passwd="passwd")

class MySQLModel(Model):
    class Meta:
        database = db
    
    @classmethod
    def load_data(cls, data_json):
        data = json.loads(data_json)
        return data

    @classmethod
    def make_from_json(cls, data_json):
        data = cls.load_data(data_json)
        return cls(**data)
    
    @classmethod
    def create_from_json(cls, data_json):
        data = cls.load_data(data_json)
        inst = cls.create(**data)
        return inst

    def get_json(self):
        return json.dumps(self.__data__)

    def __str__(self):
        return self.get_json()

class User(MySQLModel):
    id = IntegerField(primary_key=True)
    name = CharField()
    age = IntegerField()


db.connect()

data_json = json.dumps({'name':'sdfsd', 'age':'123', 'other':'sdf'})
# user = User().make_from_json(data_json)
user = User.create_from_json(data_json)
print(json.dumps({'user':user}))