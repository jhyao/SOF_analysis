from .json_model import JSONModel
from ..model2json import ModelEncoder
from peewee import SelectQuery
import logging

logger = logging.getLogger(__name__)

class JSONModel_async(JSONModel):

    manager = None

    @classmethod
    async def create_async(cls, **create):
        return await cls.manager.create(cls, **create)

    @classmethod
    async def create_from_json_async(cls, create_json):
        create = cls.load_data(create_json)
        return await cls.create(**create)
    
    @classmethod
    async def get_async(cls, *query, **kwargs):
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
    async def get_to_json_async(cls, *query, **kwargs):
        result = await cls.get(*query, **kwargs)
        return ModelEncoder(ensure_ascii=False).encode(result)
    
    @classmethod
    async def get_all_async(cls, *query, **kwargs):
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
    async def get_all_to_json_async(cls, *query, **kwargs):
        result = await cls.get_all(*query, **kwargs)
        return ModelEncoder(ensure_ascii=False).encode(result)
    
    @classmethod
    async def get_select_async(cls, query, single=False):
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
    async def get_select_to_json_async(cls, query, single=False):
        result = await cls.get_select(query, single)
        return ModelEncoder(ensure_ascii=False).encode(result)
    
    @classmethod
    async def execute_query(cls, query):
        return await cls.manager.execute(query)
    
    async def save_async(self, force_insert=False, only=None):
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

    @classmethod
    async def insert_many_execute_async(cls, rows, fields=None):
        if len(rows) == 0:
            return
        try:
            await cls.execute_query(cls.insert_many(rows))
        except Exception as e:
            logger.warning('insert many error, try insert one by one...')
            for item in rows:
                try:
                    await cls.execute_query(cls.insert(**item))
                except Exception as e:
                    logger.warning(e.__class__.__name__ + str(e.args))

    @classmethod
    async def insert_or_update_async(cls, *query, **data):
        try:
            obj = await cls.get_async(*query)
            if obj:
                cls.execute_query(cls.update(**data).where(*query))
        except cls.DoesNotExist:
            cls.execute_query(cls.insert(**data))