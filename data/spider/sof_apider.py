from .api_spider import ApiSpider
from .config import *
from .constants import *

class UsersApi(ApiSpider):
    all_params = UsersConfig.all_params
    required = UsersConfig.required
    url_pattern = UsersConfig.url_pattern

    def item_transfer(self, item):
        badges = item.pop('badge_counts', None)
        if badges:
            item['badge_bronze'] = badges['bronze']
            item['badge_silver'] = badges['silver']
            item['badge_gold'] = badges['gold']

class UsersByIdsApi(UserApi):
    url_pattern = UsersByIdsConfig.url_pattern

class AnswersApi(ApiSpider):
    all_params = AnswersConfig.all_params
    required = AnswersConfig.required
    url_pattern = AnswersConfig.url_pattern
    def item_transfer(self, item):
        owner = item.pop('owner', None)
        if owner:
            item['owner'] = owner['user_id']

class AnswersByIdsApi(AnswersApi):
    url_pattern = UrlPattern.ANSWERS_BY_IDS

class AnswersOfUsersApi(AnswersApi):
    url_pattern = UrlPattern.ANSWERS_OF_USERS

class AnswersOfQuestionsApi(AnswersApi):
    url_pattern = UrlPattern.ANSWERS_OF_QUESTIONS

class CommentsApi(ApiSpider):
    all_params = CommentsConfig.all_params
    required = CommentsConfig.required
    url_pattern = CommentsConfig.url_pattern
    def item_transfer(self, item):
        owner = item.pop('owner', None)
        if owner:
            item['owner'] = owner['user_id']


class CommentsByIdsApi(CommentsApi):
    url_pattern = UrlPattern.COMMENTS_BY_IDS


class CommentsOfUsersApi(CommentsApi):
    url_pattern = UrlPattern.COMMENTS_OF_USERS


class CommentsOfAnswersApi(CommentsApi):
    url_pattern = UrlPattern.COMMENTS_OF_ANSWERS


class CommentsOfQuestionsApi(CommentsApi):
    url_pattern = UrlPattern.COMMENTS_OF_QUESTIONS


class QuestionsApi(ApiSpider):
    all_params = QuestionsConfig.all_params
    required = QuestionsConfig.required
    url_pattern = QuestionsConfig.url_pattern
    def item_transfer(self, item):
        owner = item.pop('owner', None)
        if owner:
            item['owner'] = owner['user_id']

class QuestionsByIdsApi(QuestionsApi):
    url_pattern = UrlPattern.QUESTIONS_BY_IDS

class QuestionsOfUsersApi(QuestionsApi):
    url_pattern = UrlPattern.QUESTIONS_OF_USERS

class QuestionsOfAnswersApi(QuestionsApi):
    url_pattern = UrlPattern.QUESTIONS_OF_ANSWERS

class QuestionsLinkedApi(QuestionsApi):
    url_pattern = UrlPattern.QUESTIONS_LINKED

class QuestionsRelatedApi(QuestionsApi):
    url_pattern = UrlPattern.QUESTIONS_RELATED

class TagsApi(ApiSpider):
    all_params = TagsConfig.all_params
    required = TagsConfig.required
    url_pattern = TagsConfig.url_pattern

class TagsByNamesApi(TagsApi):
    url_pattern = UrlPattern.TAGS_BY_NAMES

class TagsOfUsersApi(TagsApi):
    url_pattern = UrlPattern.TAGS_OF_USERS

