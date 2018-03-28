from peewee import *
from .json_model_async import JSONModel_async
from ..config import config
import peewee_async

class MyModel(JSONModel_async):
    class Meta:
        database = config.pool_async

    manager = peewee_async.Manager(config.pool_async)


class Answer(MyModel):
    answer_id = IntegerField(primary_key=True)
    question_id = IntegerField()
    is_accepted = BooleanField()
    score = IntegerField()
    creation_date = TimestampField(utc=True)
    last_activity_date = TimestampField(utc=True)
    owner = IntegerField() # ForeignKeyField(User, backref='answers')


class Comment(MyModel):
    comment_id = IntegerField(primary_key=True)
    post_id = IntegerField() # ForeignKeyField(Post, backref='comments')
    creation_date = TimestampField(utc=True)
    score = IntegerField()
    edited = BooleanField()
    owner = IntegerField() # ForeignKeyField(User, backref='comments')
    replay_to_user = IntegerField() # ForeignKeyField(User, backref='comments_to_me', null=True)


class Tag(MyModel):
    name = CharField(primary_key=True)
    count = IntegerField()
    is_required = BooleanField()
    has_synonyms = BooleanField()
    is_moderator_only = BooleanField()
    from_tag = CharField()


class Question(MyModel):
    owner = IntegerField() # ForeignKeyField(User, backref='questions')
    is_answered = BooleanField()
    view_count = IntegerField()
    answer_count = IntegerField()
    score = IntegerField()
    creation_date = TimestampField(utc=True)
    last_activity_date = TimestampField(utc=True)
    question_id = IntegerField(primary_key=True)
    link = CharField()
    title = CharField()

class QuestionTags(MyModel):
    question_id = IntegerField()
    tag_id = IntegerField()

class Post(MyModel):
    post_id = IntegerField(primary_key=True)
    post_type = CharField()
    link = CharField()


class User(MyModel):
    user_id = IntegerField(primary_key=True)
    account_id = IntegerField()
    display_name = CharField()
    reputation = IntegerField()
    is_employee = BooleanField()
    last_modified_date = TimestampField(utc=True)
    last_access_date = TimestampField(utc=True)
    age = IntegerField()
    reputation_change_year = IntegerField()
    reputation_change_quarter = IntegerField()
    reputation_change_month = IntegerField()
    reputation_change_week = IntegerField()
    reputation_change_day = IntegerField()
    creation_date = IntegerField()
    user_type = CharField()
    accept_rate = IntegerField()
    location = CharField()
    website_url = CharField()
    link = CharField()
    profile_image = CharField()
    badge_bronze = IntegerField()
    badge_silver = IntegerField()
    badge_gold = IntegerField()


if __name__ == '__main__':
    config.database.connect()
    config.database.drop_tables([Answer, Question, Post, Comment])
    config.database.create_tables([Answer, Question, Post, User, Comment, Tag, QuestionTags])
    config.database.close()


