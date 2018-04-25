from data.cache.redis_cache import Cache
from data.cache.redis_keys import *
from data.models.analysis_models import TagClf
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
    def get_core_tag_clf(cls):
        tag_clf = cls.cache.get_core_tag_clf()
        if not tag_clf:
            tag_clf = {}
            for item in TagClf.select().where(TagClf.is_core==True):
                if item.clf in tag_clf:
                    tag_clf[item.clf].append(item.tag)
                else:
                    tag_clf[item.clf] = [item.tag]
            cls.set_core_tag_clf(tag_clf)
        return tag_clf

    @classmethod
    def get_tag_index(cls):
        tag_index = cls.cache.get_tag_index()
        if not tag_index:
            tag_index = {}
            for item in TagClf.select():
                tag_index[item.tag] = item.clf
            cls.cache.set_tags_category(tag_index)
        return tag_index

    @classmethod
    def get_tag_category(cls, tag):
        c = cls.cache.get_tag_category(tag)
        if not c:
            try:
                c = TagClf.get(tag=tag).clf
            except:
                pass
        return c

    @classmethod
    def set_core_tag_clf(cls, tag_clf):
        text = json.dumps(tag_clf)
        return cls.cache.set_core_tag_clf(text)

    @classmethod
    def set_tags_category(cls, tag_index):
        return cls.cache.set_tags_category(tag_index)

    @classmethod
    def set_tag_category(cls, tag, c):
        cls.cache.set_tag_category(tag, c)

    @classmethod
    def save_to_db(cls):
        tag_index = cls.get_tag_index()
        for tag in tag_index:
            TagClf.insert_or_update(TagClf.tag == tag, tag=tag, clf=tag_index[tag])


class QuestionsCDN(CDN):
    model = Question
    api = QuestionsApi
    cache = QuestionsCache

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
            question_tags = cls.dld_page(save=save, tagged=tag, sort='votes', min=0, pagesize=min_num,
                                         fromdate=date_to_timestamp('2017-01-01'),
                                         todate=date_to_timestamp('2018-04-01'))
            index = {}
            for item in question_tags:
                if item['tag'] not in index:
                    index[item['tag']] = {item['question_id']}
                else:
                    index[item['tag']].add(item['question_id'])
            for t in index:
                cls.cache.add_tag_questions(t, index[t])
            questions |= index[tag]
        return questions

    @classmethod
    def get_tag_questions_cached(cls):
        return cls.cache.get_all_tag_questions()

    @classmethod
    def load__cache(cls):
        index = {}
        for qt in QuestionTags.select():
            if qt.tag in index:
                index[qt.tag].add(qt.question_id)
            else:
                index[qt.tag] = {qt.question_id}
        cls.cache.add_tag_questions()

