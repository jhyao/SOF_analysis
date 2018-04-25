import json

from .redis_cache import Cache
import ast
from .redis_keys import Keys


class QuestionsCache(Cache):

    @classmethod
    def get_tag_questions(cls, tag):
        if cls.redis.hexists(Keys.TAG_QUESTIONS, tag):
            value = cls.redis.hget(Keys.TAG_QUESTIONS, tag)
            try:
                return ast.literal_eval(value)
            except:
                pass
        return set()

    @classmethod
    def add_tag_questions(cls, tag, questions):
        if not isinstance(questions, set):
            questions = set(questions)
        cls.redis.hset(Keys.TAG_QUESTIONS, tag, cls.get_tag_questions(tag) | questions)

    @classmethod
    def get_all_tag_questions(cls):
        if cls.redis.exists(Keys.TAG_QUESTIONS):
            value = cls.redis.hgetall(Keys.TAG_QUESTIONS)
            try:
                return ast.literal_eval(value)
            except:
                pass
        return {}

    @classmethod
    def set_tags_questions(cls, tag_questions):
        cls.redis.hmset(Keys.TAG_QUESTIONS, tag_questions)


class TagsCache(Cache):
    @classmethod
    def get_core_tag_clf(cls):
        t = cls.redis.get(Keys.CORE_TAG_CLF)
        try:
            return ast.literal_eval(t)
        except:
            return None

    @classmethod
    def get_tag_index(cls):
        text = cls.redis.hgetall(Keys.TAG_CATEGORY)
        if text:
            return text
        else:
            return None

    @classmethod
    def get_tag_category(cls, tag):
        return cls.redis.hget(Keys.TAG_CATEGORY, tag) or None

    @classmethod
    def set_core_tag_clf(cls, tag_clf_json):
        cls.redis.set(Keys.CORE_TAG_CLF, tag_clf_json)

    @classmethod
    def set_tags_category(cls, tag_index):
        cls.redis.hmset(Keys.TAG_CATEGORY, tag_index)

    @classmethod
    def set_tag_category(cls, tag, c):
        cls.redis.hset(Keys.TAG_CATEGORY, tag, c)