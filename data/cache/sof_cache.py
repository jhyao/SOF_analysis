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
    isjson = True

    @classmethod
    def get_tag_index(cls):
        return cls.hgetall({})

    @classmethod
    def get_tag_category(cls, tag):
        return cls.hget(tag)

    @classmethod
    def set_tag_category_many(cls, tag_index):
        cls.hmset(tag_index)

    @classmethod
    def set_tag_category(cls, tag, c):
        cls.hset(tag, c)


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


class TagRelatedCache(Cache):
    key = Keys.TAG_RELATED

    @staticmethod
    def get_related_name(tag1, tag2):
        return (tag1 + ' ' + tag2) if tag1 < tag2 else (tag2 + ' ' + tag1)

    @classmethod
    def set_tag_related(cls, tag1, tag2, weight=0):
        name = cls.get_related_name(tag1, tag2)
        return cls.hset(name, weight)

    @classmethod
    def set_tag_related_many(cls, tags_related):
        '''
        :param tags_related: [['a', 'b', 1], ['a', 'c', 0.5]]
        '''
        data = dict([(cls.get_related_name(item[0], item[1]), item[2]) for item in tags_related])
        return cls.hmset(data)

    @classmethod
    def get_tag_related(cls, tag1, tag2):
        return cls.hget(cls.get_related_name(tag1, tag2), default=0)

    @classmethod
    def get_tag_related_all(cls):
        return cls.hgetall(default=[])

    @classmethod
    def clear_cache(cls):
        return cls.clear()


class CoreTagClfCache(Cache):
    key = Keys.CORE_TAG_CLF
    isjson = True


class CoreTagRankCache(Cache):
    key = Keys.CORE_TAG_RANK
    isjson = True