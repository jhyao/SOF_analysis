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
    
    async def save(self, force_insert=False, only=None):
        field_dict = dict(self._data)
        if self._meta.primary_key is not False:
            pk_field = self._meta.primary_key
            pk_value = self._get_pk_value()
        else:
            pk_field = pk_value = None
        if only:
            field_dict = self._prune_fields(field_dict, only)
        elif self._meta.only_save_dirty and not force_insert:
            field_dict = self._prune_fields(
                field_dict,
                self.dirty_fields)
            if not field_dict:
                self._dirty.clear()
                return False

        self._populate_unsaved_relations(field_dict)
        if pk_value is not None and not force_insert:
            if self._meta.composite_key:
                for pk_part_name in pk_field.field_names:
                    field_dict.pop(pk_part_name, None)
            else:
                field_dict.pop(pk_field.name, None)
            rows = await self.__class__.execute_query(self.update(**field_dict).where(self._pk_expr()))
        elif pk_field is None:
            await self.__class__.execute_query(self.insert(**field_dict))
            rows = 1
        else:
            pk_from_cursor = await self.__class__.execute_query(self.insert(**field_dict))
            if pk_from_cursor is not None:
                pk_value = pk_from_cursor
            self._set_pk_value(pk_value)
            rows = 1
        self._dirty.clear()
        return rows