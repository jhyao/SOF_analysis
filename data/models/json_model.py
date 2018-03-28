from peewee import Model, SelectQuery
import json
from packaging import version


class JSONModel(Model):

    @classmethod
    def load_data(cls, data_json):
        data = json.loads(data_json, encoding='utf-8')
        return data
    
    @classmethod
    def dump_json(cls, data):
        """
        Parameters: data - list, dict, instance, instance list
        Return type: json string
        """
        if isinstance(data, cls):
            return data.get_json()
        if isinstance(data, list):
            result = []

        return json.dumps(data, ensure_ascii=False)

    @classmethod
    def make(cls, data):
        return cls(**data)

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
        # avaliable on 3.0
        insert = cls.load_data(insert_json)
        return cls.replace(insert)
    
    @classmethod
    def replace_many_from_json(cls, rows_json, fields=None):
        # avaliable on 3.0
        rows = cls.load_data(rows_json)
        return cls.replace_many(rows, fields)
    
    @classmethod
    def get_or_create_from_json(defaults_json=None, **kwargs):
        # avaliable on 3.0
        defaults = cls.load_data(defaults_json)
        return cls.get_or_create(defaults, **kwargs)

    @classmethod
    def get_select(cls, query, single=False):
        if not isinstance(query, SelectQuery):
            return None
        if single:
            return query.get()
        else:
            results = []
            for result in query:
                results.append(result)
            return results
    
    @classmethod
    def get_select_to_json(cls, query, single=False):
        if not isinstance(query, SelectQuery):
            return None
        if single:
            try:
                obj = query.get()
                return cls.dump_json(obj.get_data())
            except cls.DoesNotExist:
                return None
        else:
            results = []
            for result in query:
                results.append(result.get_data())
            return cls.dump_json(results)

    def get_data(self):
        if version.parse(peewee.__version__) > version.parse('2.10.2'):
            return self.__data__
        else:
            return self._data
    
    def get_json(self):
        return cls.dump_json(self.get_data())

    def __str__(self):
        return self.get_json()