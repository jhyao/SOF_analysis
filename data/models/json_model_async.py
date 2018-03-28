from .json_model import JSONModel
from ..model2json import ModelEncoder

class JSONModel_async(JSONModel):
 
    @classmethod
    async def get_async(cls, model, *args, **kwargs):
        return await cls.manager.get(model, *args, **kwargs)
    
    @classmethod
    async def create(cls, **create):
        return await cls.manager.create(cls, **create)

    @classmethod
    async def create_from_json(cls, create_json):
        create = cls.load_data(create_json)
        return await cls.create(cls, **create)
    
    @classmethod
    async def get(cls, *query, **kwargs):
        sq = cls.select().naive()
        if query:
            sq = sq.where(*query)
        if kwargs:
            sq = sq.filter(**kwargs)
        try:
            result = await cls.manager.execute(query)
            return list(result)[0]
        except IndexError:
            raise model.DoesNotExist
    
    @classmethod
    async def get_to_json(cls, *query, **kwargs):
        result = await cls.get(cls, *query, **kwargs)
        return cls.dump_json(result)
    
    @classmethod
    async def get_select(cls, *query, single=False):
        sq = cls.select().naive()
        if query:
            sq = sq.where(*query)
        if kwargs:
            sq = sq.filter(**kwargs)
        try:
            result = await cls.manager.execute(query)
            return list(result)
        except IndexError:
            raise model.DoesNotExist
    
    @classmethod
    async def get_select_to_json(cls, *query, single=False):
        result = await cls.get_select(*query, single=single)
        return ModelEncoder.encode(result)
    
    # @classmethod
    # async def update(cls, **update_data):
    #     return await cls.manager.update(cls.make(**update_data))

    # @classmethod
    # async def update_from_json(cls, update_json):
    #     update_data = cls.load_data(update_json)
    #     return cls.update(**update_data)