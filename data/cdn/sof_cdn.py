from .cdn import CDN
from ..models.sof_models import *
from ..spider.sof_spider import *


class UsersCDN(CDN):
    model = User
    api = UsersApi


class TagsCDN(CDN):
    model = Tag
    api = TagsApi


class QuestionsCDN(CDN):
    model = Question
    api = QuestionsApi

    @classmethod
    def dld_page(cls, **kwargs):
        page_data = cls.api(**kwargs).get()
        question_tags = [{'question_id': item['question_id'], 'tag': tag} for item in page_data for tag in
                         item.pop('tags', [])]
        cls.model.insert_many_execute(page_data)
        QuestionTags.insert_many_execute(question_tags)

    @classmethod
    async def dld_page_async(cls, **kwargs):
        page_data = await cls.api(**kwargs).get_async()
        question_tags = [{'question_id': item['question_id'], 'tag': tag} for item in page_data for tag in
                         item.pop('tags', [])]
        await cls.model.insert_many_execute_async(page_data)
        await QuestionTags.insert_many_execute_async(question_tags)
        return len(page_data)

