import time

from data.models.sof_models import *
from data.spider.sof_spider import *
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

page_from = 380
page_to = 400
page = 0

def dld_users(page_from, page_to):
    api = UsersApi(pagesize=100)
    for page in range(page_from, page_to + 1):
        logger.info(f'get user page {page}')
        page_data = []
        try:
            page_data = api.get(page=page)
        except:
            logger.error(f'get user page {page} error, try again in 10 seconds')
            time.sleep(10)
            dld_users(page, page_to)

        try:
            if page_data:
                User.insert_many(page_data).execute()
        except Exception as e:
            logger.warning('insert many error, try insert one by one...')
            for item in page_data:
                try:
                    User.insert(**item).execute()
                except Exception as e:
                    logger.warning(e.__class__.__name__ + str(e.args))
        time.sleep(0.5)


def dld_tags(page_from):
    for page_data in TagsApi(page=page_from, pagesize=100).get_pages():
        try:
            if page_data:
                Tag.insert_many(page_data).execute()
        except Exception as e:
            logger.warning('insert many error, try insert one by one...')
            for item in page_data:
                try:
                    Tag.insert(**item).execute()
                except Exception as e:
                    logger.warning(e.__class__.__name__ + str(e.args))


def dld_questions(**kwargs):
    for page_data in QuestionsApi(**kwargs).get_pages():
        if len(page_data) == 0:
            continue
        question_tags = [{'question_id': item['question_id'], 'tag': tag} for item in page_data for tag in item.pop('tags', []) ]
        Question.insert_many_execute(page_data)
        QuestionTags.insert_many_execute(question_tags)

if __name__ == '__main__':
    dld_questions(page=193, fromdate=1523404800, todate=1523491200)