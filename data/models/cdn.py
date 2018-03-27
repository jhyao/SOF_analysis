#!/usr/bin/env python
# -*- coding: utf-8 -*

"""
'cdn' means 'cache-database-network', it's the order to get data.
"""

from peewee import Model

class CDNModel(Model):
    @classmethod
    def make(cls, **data):
        """
        Make an instance of data. You can save it with method save().
        """
        pass
    
    @classmethod
    def make_from_json(cls, data_json):
        """
        Make instance with data in JSON format.
        """
        pass
    
    @classmethod
    def create_from_json(cls, create_json):
        create = cls.load_data(create_json)
        return cls.create(**create)
    
    @classmethod
    def update_from_json(cls, __data=None, update_json):
        update = cls.load_data(update_json)
        return cls.update(__data, **data)
    
    @classmethod
    def insert_from_json(cls, __data=None, insert_json):
        insert = cls.load_data(insert_json)
        return cls.insert(__data, insert)
    
    @classmethod
    def insert_many_from_json(cls, rows_json, fields=None):
        rows = cls.load_data(rows_json)
        return cls.insert_many(rows, fields)
    
    @classmethod
    def replace_from_json(cls, __data=None, insert_json):
        insert = cls.load_data(insert_json)
        return cls.replace(__data, insert)
    
    @classmethod
    def replace_many_from_json(cls, rows_json, fields=None):
        rows = cls.load_data(rows_json)
        return cls.replace_many(rows, fields)

    def get_json(self):
        return json.dumps(self.__data__)

    def __str__(self):
        return self.get_json()