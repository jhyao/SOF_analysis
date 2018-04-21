from peewee import Model, SelectQuery
import peewee
import json
from packaging import version
from ..model2json import ModelEncoder
import logging

logger = logging.getLogger(__name__)


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
        return ModelEncoder(ensure_ascii=False).encode(data)

    @classmethod
    def make(cls, **data):
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
        return cls.update(**update)
    
    @classmethod
    def insert_from_json(cls, insert_json):
        insert = cls.load_data(insert_json)
        return cls.insert(**insert)
    
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
    def get_or_create_from_json(cls, defaults_json=None, **kwargs):
        defaults = cls.load_data(defaults_json)
        return cls.get_or_create(defaults=defaults, **kwargs)
    
    @classmethod
    def get_to_json(cls, *query, **kwargs):
        return ModelEncoder(ensure_ascii=False).encode(cls.get(*query, **kwargs))
    
    @classmethod
    def get_all(cls, *query, **kwargs):
        sq = cls.select().naive()
        if query:
            sq = sq.where(*query)
        if kwargs:
            sq = sq.filter(**kwargs)
        try:
            return list(sq)
        except IndexError:
            return []
    
    @classmethod
    def get_all_to_json(cls, *query, **kwargs):
        result = cls.get_all(*query, **kwargs)
        return ModelEncoder(ensure_ascii=False).encode(result)

    @classmethod
    def get_select(cls, query, single=False):
        if not isinstance(query, SelectQuery):
            return None
        if single:
            return query.get()
        else:
            return list(query)
    
    @classmethod
    def get_select_to_json(cls, query, single=False):
        result = cls.get_select(query, single)
        return ModelEncoder(ensure_ascii=False).encode(result)

    @classmethod
    def insert_many_execute(cls, rows, fields=None):
        if len(rows) == 0:
            return
        try:
            cls.insert_many(rows).execute()
        except Exception as e:
            logger.warning('insert many error, try insert one by one...')
            for item in rows:
                try:
                    cls.insert(**item).execute()
                except Exception as e:
                    logger.warning(e.__class__.__name__ + str(e.args))

    @classmethod
    def insert_or_update(cls, *query, **data):
        try:
            obj = cls.get(*query)
            if obj:
                cls.update(**data).where(*query).execute()
        except cls.DoesNotExist:
            cls.insert(**data).execute()

    @classmethod
    def insert_if_not_exist(cls, *query, **data):
        try:
            obj = cls.get(*query)
        except cls.DoesNotExist:
            cls.insert(**data).execute()

    def get_data(self):
        if version.parse(peewee.__version__) > version.parse('2.10.2'):
            return self.__data__
        else:
            return self._data
    
    def get_json(self):
        return ModelEncoder(ensure_ascii=False).encode(self)

    def __str__(self):
        return self.get_json()
