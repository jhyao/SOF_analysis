import peewee_async
from peewee import *
from data.config.config import Config
from data.models.json_model_async import JSONModel_async

import logging
logger = logging.getLogger(__name__)

config = Config('analysis')

class MyModel(JSONModel_async):
    class Meta:
        database = config.pool_async

    manager = peewee_async.Manager(config.pool_async)


class TagRelated(MyModel):
    tag_from = IntegerField(index=True)
    tag_to = IntegerField(index=True)
    weight = DoubleField(null=True)


class TagClf(MyModel):
    tag = CharField(primary_key=True)
    clf = TextField()
    is_core = BooleanField(default=False)


class UserTags(MyModel):
    user_id = IntegerField(index=True)
    tag = CharField()
    question_count = IntegerField(default=0)
    question_score = IntegerField(default=0)
    answer_count = IntegerField(default=0)
    answer_score = IntegerField(default=0)

if __name__ == '__main__':
    root = Config('analysis')

    root.database.connect()
    root.database.drop_tables([TagClf])
    root.database.create_tables([TagClf])
    root.database.close()