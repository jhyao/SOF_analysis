import json

from .redis_cache import Cache
import ast
from .redis_keys import Keys


class TagQuestionsCache(Cache):
    key = Keys.TAG_QUESTIONS
    @classmethod
    def get_tag_questions(cls, tag):
        return cls.hget(tag, set())

    @classmethod
    def add_tag_questions(cls, tag, questions):
        if not isinstance(questions, set):
            questions = set(questions)
        cls.hset(tag, cls.get_tag_questions(tag) | questions)

    @classmethod
    def get_all_tag_questions(cls):
        return cls.hgetall({})

    @classmethod
    def set_tags_questions_many(cls, tag_questions):
        cls.redis.hmset(cls.key, tag_questions)

    @classmethod
    def get_tags_questions_many(cls, tags):
        cls.hmget(tags, {})


class TagsCache(Cache):
    key = Keys.TAG_CATEGORY
    @classmethod
    def get_core_tag_clf(cls):
        t = cls.redis.get(Keys.CORE_TAG_CLF)
        try:
            return ast.literal_eval(t)
        except:
            return None

    @classmethod
    def get_tag_index(cls):
        return cls.hgetall({})

    @classmethod
    def get_tag_category(cls, tag):
        return cls.hget(tag, isjson=True)

    @classmethod
    def set_core_tag_clf(cls, tag_clf):
        cls.set(Keys.CORE_TAG_CLF, tag_clf, to_json=True)

    @classmethod
    def set_tag_category_many(cls, tag_index):
        cls.hmset(tag_index, to_json=True)

    @classmethod
    def set_tag_category(cls, tag, c):
        cls.hset(tag, c, to_json=True)


class UserTagsCache(Cache):
    key = Keys.USER_TAGS

    @classmethod
    def get_user_tags(cls, user_id):
        return cls.hget(str(user_id), [])

    @classmethod
    def set_user_tags(cls, user_id, tags):
        return cls.hset(str(user_id), tags)

    @classmethod
    def set_user_tags_many(cls, user_tags):
        return cls.hmset(user_tags)