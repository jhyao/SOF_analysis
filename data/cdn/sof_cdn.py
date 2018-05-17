from data.cache.redis_cache import Cache
from data.cache.redis_keys import *
from data.models.analysis_models import TagClf, UserTags, TagRelated
from utils.date_transfer import date_to_timestamp
from .cdn import CDN
from ..models.sof_models import *
from ..spider.sof_spider import *
from ..cache.sof_cache import *

logger = logging.getLogger(__name__)


class UsersCDN(CDN):
    model = User
    api = UsersApi


class TagsCDN(CDN):
    model = Tag
    api = TagsApi
    cache = TagsCache

    @classmethod
    def get_tag_index(cls):
        tag_index = cls.cache.get_tag_index()
        if not tag_index:
            tag_index = {}
            for item in TagClf.select():
                tag_index[item.tag] = item.clf
            cls.cache.set_tag_category_many(tag_index)
        return tag_index

    @classmethod
    def get_tag_category(cls, tag, from_db=True):
        c = cls.cache.get_tag_category(tag)
        if not c and from_db:
            try:
                c = json.loads(TagClf.get(tag=tag).clf)
                cls.set_tag_category(tag, c)
            except:
                pass
        return c

    @classmethod
    def set_tag_category_many(cls, tag_index):
        return cls.cache.set_tag_category_many(tag_index)

    @classmethod
    def set_tag_category(cls, tag, c, to_db=True):
        is_core = c.get('is_core', False)
        cls.cache.set_tag_category(tag, c)
        if to_db:
            TagClf.insert_or_update(TagClf.tag == tag, tag=tag, clf=json.dumps(c), is_core=is_core)

    @classmethod
    def save_to_db(cls):
        tag_index = cls.get_tag_index()
        for tag in tag_index:
            TagClf.insert_or_update(TagClf.tag == tag, tag=tag, clf=tag_index[tag])

    @classmethod
    def get_tags(cls, limit=None):
        # get tags order by question count
        return [tag.name for tag in Tag.select(Tag.name).order_by(-Tag.count).limit(limit)]

    @classmethod
    def clear_tag_category(cls):
        cls.cache.clear()
        TagClf.truncate_table()

    @classmethod
    def del_tag_category(cls, tag):
        cls.cache.hdel(tag)
        TagClf.delete().where(TagClf.tag==tag).execute()


class QuestionsCDN(CDN):
    model = Question
    api = QuestionsApi
    cache = TagQuestionsCache

    @classmethod
    def dld_page(cls, save=True, **kwargs):
        page_data = cls.api(**kwargs).get()
        question_tags = [{'question_id': item['question_id'], 'tag': tag} for item in page_data for tag in
                         item.pop('tags', [])]
        if save:
            cls.model.insert_many_execute(page_data)
            QuestionTags.insert_many_execute(question_tags)
        return question_tags

    @classmethod
    async def dld_page_async(cls, save=True, **kwargs):
        page_data = await cls.api(**kwargs).get_async()
        question_tags = [{'question_id': item['question_id'], 'tag': tag} for item in page_data for tag in
                         item.pop('tags', [])]
        if save:
            await cls.model.insert_many_execute_async(page_data)
            await QuestionTags.insert_many_execute_async(question_tags)
        return len(page_data)

    @classmethod
    def get_tag_questions(cls, tag, save=True, from_cache=True, from_db=True, from_api=True, min_num=50):
        if from_cache:
            questions = cls.cache.get_tag_questions(tag)
            logger.info(f'get {tag} questions from cache')
        else:
            questions = set()

        if len(questions) < min_num and from_db:
            logger.info(f'get {tag} questions from db')
            l_old = len(questions)
            questions |= {q.question_id for q in QuestionTags.select(QuestionTags.question_id).where(QuestionTags.tag == tag)}
            if len(questions) > l_old:
                cls.cache.add_tag_questions(tag, questions)
        if len(questions) < min_num and from_api:
            logger.info(f'get {tag} questions from api')
            # question_tags = cls.dld_pages(save=save, tagged=tag, sort='votes', min=0, pagesize=100, max_page=min_num//100+1,
            #                              fromdate=date_to_timestamp('2017-01-01'),
            #                              todate=date_to_timestamp('2018-04-01'))
            question_tags = cls.dld_pages(save=save, tagged=tag, sort='votes', pagesize=100,
                                          max_page=min_num // 100 + (1 if min_num % 100 > 0 else 0))
            index = {}
            for item in question_tags:
                if item['tag'] not in index:
                    index[item['tag']] = {item['question_id']}
                else:
                    index[item['tag']].add(item['question_id'])
            for t in index:
                cls.cache.add_tag_questions(t, index[t])
            questions |= index.get(tag, set())
        return questions

    @classmethod
    def get_tag_questions_cached(cls):
        return cls.cache.get_all_tag_questions()

    @classmethod
    def load_to_cache(cls):
        index = {}
        for qt in QuestionTags.select():
            if qt.tag in index:
                index[qt.tag].add(qt.question_id)
            else:
                index[qt.tag] = {qt.question_id}
        for t in index:
            cls.cache.add_tag_questions(t, index[t])

    @classmethod
    def save_to_db(cls):
        tag_questions = cls.get_tag_questions_cached()
        QuestionTags.truncate_table()
        insert_set = []
        for tag in tag_questions:
            insert_set.extend([{'question_id': question, 'tag': tag} for question in tag_questions[tag]])
            if len(insert_set) > 500:
                QuestionTags.insert_many_execute(insert_set)
                insert_set.clear()
        QuestionTags.insert_many_execute(insert_set)


    @classmethod
    def tags_have_questions(cls, min_questions=100):
        tag_questions = cls.get_tag_questions_cached()
        return [tag for tag in tag_questions if len(tag_questions[tag]) > min_questions]

    @classmethod
    def get_tag_questions_filtered(cls, min_question=100):
        tag_questions = cls.get_tag_questions_cached()
        for tag in list(tag_questions.keys()):
            if len(tag_questions[tag]) < min_question:
                tag_questions.pop(tag)
        return tag_questions

class UserTagsCDN(CDN):
    model = UserTags
    api = UserTagsApi
    cache = UserTagsCache

    @classmethod
    def get_user_tags(cls, user_id, save=True, from_cache=True, from_db=True, from_api=True):
        if from_cache:
            tags = cls.cache.get_user_tags(user_id)
            logger.debug(f'get user ({user_id}) tags from cache')
        else:
            tags = {}
        if not tags and from_db:
            logger.debug(f'get user ({user_id}) tags from db')
            tags = cls.model.get_select_to_dict(cls.model.user_id == user_id)
            if tags:
                cls.cache.set_user_tags(user_id, tags)
        if not tags and from_api:
            logger.debug(f'get user ({user_id}) tags from api')
            tags = cls.dld_pages(save=save, user_ids=[user_id])
            cls.cache.set_user_tags(user_id, tags)
        return tags

class TagRelatedCDN(CDN):
    model = TagRelated
    api = None
    cache = TagRelatedCache

    @classmethod
    def set_tag_related(cls, tag1, tag2, weight=0):
        return cls.cache.set_tag_related(tag1, tag2, weight)

    @classmethod
    def set_tag_related_many(cls, tags_related):
        '''
        :param tags_related: [['a', 'b', 1], ['a', 'c', 0.5]]
        '''
        return cls.cache.set_tag_related_many(tags_related)

    @classmethod
    def get_related_weight(cls, tag1, tag2):
        return cls.cache.get_tag_related(tag1, tag2)

    @classmethod
    def get_related_weight_all(cls):
        data = cls.cache.get_tag_related_all()
        return [[name.split()[0], name.split()[1], data[name]] for name in data]

    @classmethod
    def get_tag_related_filtered(cls, min_weight=0.2):
        return list(filter(lambda item: item[2] >= min_weight, cls.get_related_weight_all()))

    @classmethod
    def clear_cache(cls):
        cls.cache.clear()

