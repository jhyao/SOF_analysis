from .constants import *

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
    USERS_BY_IDS = 'users/{keys}'

    ANSWERS = 'answers'
    ANSWERS_BY_IDS = 'answers/{keys}'
    ANSWERS_OF_USERS = 'users/{keys}/answers'
    ANSWERS_OF_QUESTIONS = 'questions/{keys}/answers'

    COMMENTS = 'comments'
    COMMENTS_BY_IDS = 'comments/{keys}'
    COMMENTS_OF_USERS = 'users/{keys}/comments'
    COMMENTS_OF_POSTS = 'posts/{keys}/comments'
    COMMENTS_OF_ANSWERS = 'answers/{keys}/comments'
    COMMENTS_OF_QUESTIONS = 'questions/{keys}/comments'

    QUESTIONS = 'questions'
    QUESTIONS_BY_IDS = 'questions/{keys}'
    QUESTIONS_OF_USERS = 'users/{keys}/questions'
    QUESTIONS_OF_ANSWERS = 'answers/{keys}/questions'
    QUESTIONS_LINKED = 'questions/{keys}/linked'
    QUESTIONS_RELATED = 'questions/{keys}/related'
    QUESTIONS_OF_TAGS = 'tags/{keys}/faq'
    QUESTIONS_FEATURED = 'questions/featured'
    QUESTIONS_UNANSWERED = 'questions/unanswered'
    QUESTIONS_SIMILAR = 'similar'
    QUESTIONS_SEARCH = 'search'

    POSTS = 'posts'
    POSTS_BY_IDS = 'posts/{keys}'
    POSTS_OF_USERS = 'users/{keys}/posts'

    TAGS = 'tags'
    TAGS_BY_NAMES = 'tags/{keys}/info'
    TAGS_OF_USERS = 'users/{keys}/tags'

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

class UsersConfig(DefaultConfig):
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

class AnswersConfig(DefaultConfig):
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


class CommentsConfig(DefaultConfig):
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

class QuestionsConfig(DefaultConfig):
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

class TagsConfig(DefaultConfig):
    all_params = {
        Param.PAGE: 1,
        Param.PAGESIZE: 50,
        Param.FROMDATE: None,
        Param.TODATE: None,
        Param.ORDER: Order.DESC,
        Param.MIN: None,
        Param.MAX: None,
        Param.SORT: Sort.POPULAR,
        Param.SITE: 'stackoverflow'
    }
    required = [Param.ORDER, Param.SORT, Param.SITE]
    url_pattern = UrlPattern.TAGS