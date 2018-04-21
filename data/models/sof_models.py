import logging
from peewee import *
from .json_model_async import JSONModel_async
import peewee_async

from ..config.config import config, Config

logger = logging.getLogger(__name__)


class MyModel(JSONModel_async):
    class Meta:
        database = config.pool_async

    manager = peewee_async.Manager(config.pool_async)


class Answer(MyModel):
    answer_id = IntegerField(primary_key=True)
    question_id = IntegerField(null=True)
    is_accepted = BooleanField(null=True)
    score = IntegerField(null=True)
    creation_date = TimestampField(utc=True, null=True)
    last_activity_date = TimestampField(utc=True, null=True)
    owner = IntegerField(null=True) # ForeignKeyField(User, backref='answers')


class Comment(MyModel):
    comment_id = IntegerField(primary_key=True)
    post_id = IntegerField(null=True) # ForeignKeyField(Post, backref='comments')
    creation_date = TimestampField(utc=True, null=True)
    score = IntegerField(null=True)
    edited = BooleanField(null=True)
    owner = IntegerField(null=True) # ForeignKeyField(User, backref='comments')
    replay_to_user = IntegerField(null=True) # ForeignKeyField(User, backref='comments_to_me', null=True)


class Tag(MyModel):
    name = CharField(primary_key=True)
    count = IntegerField(null=True)
    is_required = BooleanField(null=True)
    has_synonyms = BooleanField(null=True)
    is_moderator_only = BooleanField(null=True)
    from_tag = CharField(null=True)
    id = IntegerField(null=True)


class Question(MyModel):
    owner = IntegerField(null=True) # ForeignKeyField(User, backref='questions')
    is_answered = BooleanField(null=True)
    view_count = IntegerField(null=True)
    answer_count = IntegerField(null=True)
    score = IntegerField(null=True)
    creation_date = TimestampField(utc=True, null=True)
    last_activity_date = TimestampField(utc=True, null=True)
    question_id = IntegerField(primary_key=True)
    link = CharField(null=True)
    title = CharField(null=True)

class QuestionTags(MyModel):
    question_id = IntegerField(index=True)
    tag = CharField(index=True)

class Post(MyModel):
    post_id = IntegerField(primary_key=True)
    post_type = CharField(null=True)
    link = CharField(null=True)


class User(MyModel):
    user_id = IntegerField(primary_key=True)
    badge_bronze = IntegerField(null=True)
    badge_silver = IntegerField(null=True)
    badge_gold = IntegerField(null=True)
    account_id = IntegerField(null=True)
    is_employee = BooleanField(null=True)
    last_modified_date = TimestampField(utc=True, null=True)
    last_access_date = TimestampField(utc=True, null=True)
    age = IntegerField(null=True)
    reputation_change_year = IntegerField(null=True)
    reputation_change_quarter = IntegerField(null=True)
    reputation_change_month = IntegerField(null=True)
    reputation_change_week = IntegerField(null=True)
    reputation_change_day = IntegerField(null=True)
    reputation = IntegerField(null=True)
    creation_date = IntegerField(null=True)
    user_type = CharField(null=True)
    accept_rate = IntegerField(null=True)
    location = CharField(null=True)
    website_url = CharField(null=True)
    link = CharField(null=True)
    profile_image = CharField(null=True)
    display_name = CharField(null=True)


if __name__ == '__main__':
    root = Config('root')

    root.database.connect()
    root.database.drop_tables([Answer, Question, Post, User, Comment, Tag, QuestionTags])
    root.database.create_tables([Answer, Question, Post, User, Comment, Tag, QuestionTags])
    root.database.close()


