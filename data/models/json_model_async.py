from .json_model import JSONModel
from ..model2json import ModelEncoder
import asyncio
from peewee import SelectQuery

class JSONModel_async(JSONModel):

    @classmethod
    async def create(cls, **create):
        return await cls.manager.create(cls, **create)

    @classmethod
    async def create_from_json(cls, create_json):
        create = cls.load_data(create_json)
        return await cls.create(**create)
    
    @classmethod
    async def get(cls, *query, **kwargs):
        sq = cls.select().naive()
        if query:
            sq = sq.where(*query)
        if kwargs:
            sq = sq.filter(**kwargs)
        try:
            result = await cls.manager.execute(sq)
            return list(result)[0]
        except IndexError:
            raise cls.DoesNotExist
    
    @classmethod
    async def get_to_json(cls, *query, **kwargs):
        result = await cls.get(*query, **kwargs)
        return ModelEncoder(ensure_ascii=False).encode(result)
    
    @classmethod
    async def get_all(cls, *query, **kwargs):
        sq = cls.select().naive()
        if query:
            sq = sq.where(*query)
        if kwargs:
            sq = sq.filter(**kwargs)
        try:
            result = await cls.manager.execute(sq)
            return list(result)
        except IndexError:
            return []
    
    @classmethod
    async def get_all_to_json(cls, *query, **kwargs):
        result = await cls.get_all(*query, **kwargs)
        return ModelEncoder(ensure_ascii=False).encode(result)
    
    @classmethod
    async def get_select(cls, query, single=False):
        if not isinstance(query, SelectQuery):
            return None
        result = await cls.execute_query(query)
        if single:
            try:
                return list(result)[0]
            except IndexError:
                raise cls.DoesNotExist
        else:
            return list(result)
    
    @classmethod
    async def get_select_to_json(cls, query, single=False):
        result = await cls.get_select(query, single)
        return ModelEncoder(ensure_ascii=False).encode(result)
    
    @classmethod
    async def execute_query(cls, query):
        return await cls.manager.execute(query)
    
    # @classmethod
    # async def update(cls, **update_data):
    #     return await cls.manager.update(cls.make(**update_data))

    # @classmethod
    # async def update_from_json(cls, update_json):
    #     update_data = cls.load_data(update_json)
    #     return cls.update(**update_data)