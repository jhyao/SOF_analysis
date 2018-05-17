from ..config import spider_config
from .api_spider import ApiSpider
import logging

logger = logging.getLogger(__name__)

class UsersApi(ApiSpider):
    config = spider_config.UsersConfig

    def item_transfer(self, item):
        badges = item.pop('badge_counts', None)
        if badges:
            item['badge_bronze'] = badges['bronze']
            item['badge_silver'] = badges['silver']
            item['badge_gold'] = badges['gold']


class UsersByIdsApi(UsersApi):
    config = spider_config.UsersByIdsConfig


class AnswersApi(ApiSpider):
    config = spider_config.AnswersConfig

    def item_transfer(self, item):
        owner = item.pop('owner', None)
        if owner:
            item['owner'] = owner['user_id']


class AnswersByIdsApi(AnswersApi):
    config = spider_config.AnswersByIdsConfig


class AnswersOfUsersApi(AnswersApi):
    config = spider_config.AnswersOfUsersConfig


class AnswersOfQuestionsApi(AnswersApi):
    config = spider_config.AnswersOfQuestionsConfig


class CommentsApi(ApiSpider):
    config = spider_config.CommentsConfig

    def item_transfer(self, item):
        owner = item.pop('owner', None)
        if owner:
            item['owner'] = owner['user_id']


class CommentsByIdsApi(CommentsApi):
    config = spider_config.CommentsByIdsConfig


class CommentsOfUsersApi(CommentsApi):
    config = spider_config.CommentsOfUsersConfig


class CommentsOfAnswersApi(CommentsApi):
    config = spider_config.CommentsOfAnswersConfig


class CommentsOfQuestionsApi(CommentsApi):
    config = spider_config.CommentsOfQuestionsConfig


class QuestionsApi(ApiSpider):
    config = spider_config.QuestionsConfig

    def item_transfer(self, item):
        owner = item.pop('owner', None)
        if owner:
            item['owner'] = owner.get('user_id', None)


class QuestionsByIdsApi(QuestionsApi):
    config = spider_config.QuestionsByIdsConfig


class QuestionsOfUsersApi(QuestionsApi):
    config = spider_config.QuestionsOfUsersConfig


class QuestionsOfAnswersApi(QuestionsApi):
    config = spider_config.QuestionsOfAnswersConfig


class QuestionsLinkedApi(QuestionsApi):
    config = spider_config.QuestionsLinkedConfig


class QuestionsRelatedApi(QuestionsApi):
    config = spider_config.QuestionsRelatedConfig


class QuestionsOfTagsApi(QuestionsApi):
    config = spider_config.QuestionsOfTagsConfig


class QuestionsFeaturedApi(QuestionsApi):
    config = spider_config.QuestionsFeaturedConfig


class QuestionsUnansweredApi(QuestionsApi):
    config = spider_config.QuestionsUnansweredConfig


class QuestionsSimilarApi(QuestionsApi):
    config = spider_config.QuestionsSimilarConfig


class QuestionsSearchApi(QuestionsApi):
    config = spider_config.QuestionsSearchConfig


class TagsApi(ApiSpider):
    config = spider_config.TagsConfig


class TagsByNamesApi(TagsApi):
    config = spider_config.TagsByNamesConfig


class UserTagsApi(TagsApi):
    config = spider_config.UserTagsConfig

    def item_transfer(self, item):
        item['tag'] = item.pop('tag_name')


class TagsSynonymsApi(ApiSpider):
    config = spider_config.TagsSynonymsConfig
