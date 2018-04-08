from .spider_constants import *

all_params_default = {
    Param.PAGE: 1,
    Param.PAGESIZE: 50,
    Param.FROMDATE: None,
    Param.TODATE: None,
    Param.ORDER: Order.DESC,
    Param.MIN: None,
    Param.MAX: None,
    Param.SORT: Sort.REPUTATION,
    Param.SITE: 'stackoverflow'
}
required_default = [Param.ORDER, Param.SORT, Param.SITE]
api_url = 'https://api.stackexchange.com/2.2/'

class UrlPattern(object):
    USERS = 'users'
    USERS_BY_IDS = 'users/{user_ids}'

    ANSWERS = 'answers'
    ANSWERS_BY_IDS = 'answers/{answer_ids}'
    ANSWERS_OF_USERS = 'users/{user_ids}/answers'
    ANSWERS_OF_QUESTIONS = 'questions/{question_ids}/answers'

    COMMENTS = 'comments'
    COMMENTS_BY_IDS = 'comments/{comment_ids}'
    COMMENTS_OF_USERS = 'users/{user_ids}/comments'
    COMMENTS_OF_POSTS = 'posts/{post_ids}/comments'
    COMMENTS_OF_ANSWERS = 'answers/{answer_ids}/comments'
    COMMENTS_OF_QUESTIONS = 'questions/{question_ids}/comments'

    QUESTIONS = 'questions'
    QUESTIONS_BY_IDS = 'questions/{question_ids}'
    QUESTIONS_OF_USERS = 'users/{user_ids}/questions'
    QUESTIONS_OF_ANSWERS = 'answers/{answer_ids}/questions'
    QUESTIONS_LINKED = 'questions/{question_ids}/linked'
    QUESTIONS_RELATED = 'questions/{question_ids}/related'
    QUESTIONS_OF_TAGS = 'tags/{tag_names}/faq'
    QUESTIONS_FEATURED = 'questions/featured'
    QUESTIONS_UNANSWERED = 'questions/unanswered'
    QUESTIONS_SIMILAR = 'similar'
    QUESTIONS_SEARCH = 'search'

    POSTS = 'posts'
    POSTS_BY_IDS = 'posts/{post_ids}'
    POSTS_OF_USERS = 'users/{user_ids}/posts'

    TAGS = 'tags'
    TAGS_BY_NAMES = 'tags/{tag_names}/info'
    TAGS_OF_USERS = 'users/{user_ids}/tags'


class DefaultConfig(object):
    all_params = {
        Param.PAGE: 1,
        Param.PAGESIZE: 50,
        Param.FROMDATE: None,
        Param.TODATE: None,
        Param.ORDER: Order.DESC,
        Param.MIN: None,
        Param.MAX: None,
        Param.SORT: None,
        Param.SITE: 'stackoverflow'
    }
    required = [Param.ORDER, Param.SITE]
    url_pattern = None
    keys_required = []


class UsersConfig(DefaultConfig):
    sorts = [
        Sort.REPUTATION,
        Sort.CREATION,
        Sort.NAME,
        Sort.MODIFIED
    ]
    all_params = {
        Param.PAGE: 1,
        Param.PAGESIZE: 50,
        Param.FROMDATE: None,
        Param.TODATE: None,
        Param.ORDER: Order.DESC,
        Param.MIN: None,
        Param.MAX: None,
        Param.SORT: Sort.REPUTATION,
        Param.SITE: 'stackoverflow'
    }
    required = [Param.ORDER, Param.SORT, Param.SITE]
    url_pattern = UrlPattern.USERS
    fields = {
        "badge_bronze": 0,
        "badge_silver": 0,
        "badge_gold": 0,
        "account_id": None,
        "is_employee": False,
        "last_modified_date": None,
        "last_access_date": None,
        "age": None,
        "reputation_change_year": 0,
        "reputation_change_quarter": 0,
        "reputation_change_month": 0,
        "reputation_change_week": 0,
        "reputation_change_day": 0,
        "reputation": 0,
        "creation_date": None,
        "user_type": None,
        "user_id": None,
        "accept_rate": None,
        "location": None,
        "website_url": None,
        "link": None,
        "profile_image": None,
        "display_name": None
    }


class UsersByIdsConfig(UsersConfig):
    url_pattern = UrlPattern.USERS_BY_IDS
    keys_required = ['user_ids']


class AnswersConfig(DefaultConfig):
    sorts = [
        Sort.ACTIVITY,
        Sort.CREATION,
        Sort.VOTES
    ]
    all_params = {
        Param.PAGE: 1,
        Param.PAGESIZE: 50,
        Param.FROMDATE: None,
        Param.TODATE: None,
        Param.ORDER: Order.DESC,
        Param.MIN: None,
        Param.MAX: None,
        Param.SORT: Sort.ACTIVITY,
        Param.SITE: 'stackoverflow'
    }
    required = [Param.ORDER, Param.SORT, Param.SITE]
    url_pattern = UrlPattern.ANSWERS


class AnswersByIdsConfig(AnswersConfig):
    url_pattern = UrlPattern.ANSWERS_BY_IDS
    keys_required = ['answer_ids']


class AnswersOfUsersConfig(AnswersConfig):
    url_pattern = UrlPattern.ANSWERS_OF_USERS
    keys_required = ['user_ids']


class AnswersOfQuestionsConfig(AnswersConfig):
    url_pattern = UrlPattern.ANSWERS_OF_QUESTIONS
    keys_required = ['question_ids']


class CommentsConfig(DefaultConfig):
    sorts = [
        Sort.CREATION,
        Sort.VOTES
    ]
    all_params = {
        Param.PAGE: 1,
        Param.PAGESIZE: 50,
        Param.FROMDATE: None,
        Param.TODATE: None,
        Param.ORDER: Order.DESC,
        Param.MIN: None,
        Param.MAX: None,
        Param.SORT: Sort.CREATION,
        Param.SITE: 'stackoverflow'
    }
    required = [Param.ORDER, Param.SORT, Param.SITE]
    url_pattern = UrlPattern.COMMENTS


class CommentsByIdsConfig(CommentsConfig):
    url_pattern = UrlPattern.COMMENTS_BY_IDS
    keys_required = ['comment_ids']


class CommentsOfUsersConfig(CommentsConfig):
    url_pattern = UrlPattern.COMMENTS_OF_USERS
    keys_required = ['user_ids']


class CommentsOfAnswersConfig(CommentsConfig):
    url_pattern = UrlPattern.COMMENTS_OF_ANSWERS
    keys_required = ['answer_ids']


class CommentsOfQuestionsConfig(CommentsConfig):
    url_pattern = UrlPattern.COMMENTS_OF_QUESTIONS
    keys_required = ['question_ids']


class CommentsOfPostsConfig(CommentsConfig):
    url_pattern = UrlPattern.COMMENTS_OF_POSTS
    keys_required = ['post_ids']


class QuestionsBaseConfig(DefaultConfig):
    sorts = [
        Sort.ACTIVITY,
        Sort.CREATION,
        Sort.VOTES
    ]
    all_params = {
        Param.PAGE: 1,
        Param.PAGESIZE: 50,
        Param.FROMDATE: None,
        Param.TODATE: None,
        Param.ORDER: Order.DESC,
        Param.MIN: None,
        Param.MAX: None,
        Param.SORT: Sort.ACTIVITY,
        Param.SITE: 'stackoverflow'
    }
    required = [Param.ORDER, Param.SORT, Param.SITE]
    url_pattern = UrlPattern.QUESTIONS


class QuestionsConfig(QuestionsBaseConfig):
    sorts = [
        Sort.ACTIVITY,
        Sort.CREATION,
        Sort.VOTES,
        Sort.HOT,
        Sort.WEEK,
        Sort.MONTH
    ]
    url_pattern = UrlPattern.QUESTIONS


class QuestionsByIdsConfig(QuestionsBaseConfig):
    url_pattern = UrlPattern.QUESTIONS_BY_IDS
    keys_required = ['question_ids']


class QuestionsOfUsersConfig(QuestionsBaseConfig):
    url_pattern = UrlPattern.QUESTIONS_OF_USERS
    keys_required = ['user_ids']


class QuestionsOfAnswersConfig(QuestionsBaseConfig):
    url_pattern = UrlPattern.QUESTIONS_OF_ANSWERS
    keys_required = ['answer_ids']


class QuestionsLinkedConfig(QuestionsBaseConfig):
    sorts = [
        Sort.ACTIVITY,
        Sort.CREATION,
        Sort.VOTES,
        Sort.RANK # a priority sort by site applies, subject to change at any time
    ]
    url_pattern = UrlPattern.QUESTIONS_LINKED
    keys_required = ['question_ids']


class QuestionsRelatedConfig(QuestionsBaseConfig):
    sorts = [
        Sort.ACTIVITY,
        Sort.CREATION,
        Sort.VOTES,
        Sort.RANK # a priority sort by site applies, subject to change at any time
    ]
    url_pattern = UrlPattern.QUESTIONS_RELATED
    keys_required = ['question_ids']


class QuestionsOfTagsConfig(QuestionsBaseConfig):
    sorts = []
    all_params = {
        Param.PAGE: 1,
        Param.PAGESIZE: 50,
        Param.SITE: 'stackoverflow'
    }
    required = []
    url_pattern = UrlPattern.QUESTIONS_OF_TAGS
    keys_required = ['tag_names']


class QuestionsFeaturedConfig(QuestionsBaseConfig):
    all_params = {
        Param.PAGE: 1,
        Param.PAGESIZE: 50,
        Param.FROMDATE: None,
        Param.TODATE: None,
        Param.ORDER: Order.DESC,
        Param.MIN: None,
        Param.MAX: None,
        Param.SORT: None,
        Param.SITE: 'stackoverflow',
        Param.TAGGED : None
    }
    url_pattern = UrlPattern.QUESTIONS_FEATURED


class QuestionsUnansweredConfig(QuestionsBaseConfig):
    all_params = {
        Param.PAGE: 1,
        Param.PAGESIZE: 50,
        Param.FROMDATE: None,
        Param.TODATE: None,
        Param.ORDER: Order.DESC,
        Param.MIN: None,
        Param.MAX: None,
        Param.SORT: None,
        Param.SITE: 'stackoverflow',
        Param.TAGGED : None
    }
    url_pattern = UrlPattern.QUESTIONS_UNANSWERED


class QuestionsSimilarConfig(QuestionsBaseConfig):
    sorts = [
        Sort.ACTIVITY,
        Sort.CREATION,
        Sort.VOTES,
        Sort.RELEVANCE # order by "how similar" the questions are, most likely candidate first with a descending order
    ]
    all_params = {
        Param.PAGE: 1,
        Param.PAGESIZE: 50,
        Param.FROMDATE: None,
        Param.TODATE: None,
        Param.ORDER: Order.DESC,
        Param.MIN: None,
        Param.MAX: None,
        Param.SORT: None,
        Param.SITE: 'stackoverflow',
        Param.TAGGED : None,
        Param.NOTAGGED: None,
        Param.TITLE: None
    }
    url_pattern = UrlPattern.QUESTIONS_SIMILAR


class QuestionsSearchConfig(QuestionsBaseConfig):
    sorts = [
        Sort.ACTIVITY,
        Sort.CREATION,
        Sort.VOTES,
        Sort.RELEVANCE # order by "how similar" the questions are, most likely candidate first with a descending order
    ]
    all_params = {
        Param.PAGE: 1,
        Param.PAGESIZE: 50,
        Param.FROMDATE: None,
        Param.TODATE: None,
        Param.ORDER: Order.DESC,
        Param.MIN: None,
        Param.MAX: None,
        Param.SORT: None,
        Param.SITE: 'stackoverflow',
        Param.TAGGED : None,
        Param.NOTAGGED: None,
        Param.INTITLE: None
    }
    url_pattern = UrlPattern.QUESTIONS_SEARCH


class TagsConfig(DefaultConfig):
    sorts = [
        Sort.POPULAR,
        Sort.ACTIVITY,
        Sort.NAME
    ]
    all_params = {
        Param.PAGE: 1,
        Param.PAGESIZE: 50,
        Param.FROMDATE: None,
        Param.TODATE: None,
        Param.ORDER: Order.DESC,
        Param.MIN: None,
        Param.MAX: None,
        Param.SORT: Sort.POPULAR,
        Param.SITE: 'stackoverflow',
        Param.INNAME: None
    }
    required = [Param.ORDER, Param.SORT, Param.SITE]
    url_pattern = UrlPattern.TAGS


class TagsByNamesConfig(DefaultConfig):
    url_pattern = UrlPattern.TAGS_BY_NAMES
    keys_required = ['tag_names']


class TagsOfUsersConfig(DefaultConfig):
    url_pattern = UrlPattern.TAGS_OF_USERS
    keys_required = ['user_ids']

