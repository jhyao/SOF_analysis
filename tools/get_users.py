import logging
from data.spider.sof_spider import UsersApi
from data.models.sof_models import User
import asyncio

logger = logging.getLogger(__name__)

async def get_users(page_from, page_to):
    if page_to < page_from:
        return
    max_pages = page_to - page_from + 1
    page = page_from
    for page_data in UsersApi().get_pages(page=page_from, max_pages=max_pages):
        logger.info(f'get page {page}')
        page += 1
        try:
            await User.execute_query(User.insert_many(page_data))
        except Exception as e:
            logger.warning('insert many error, try insert one by one...')
            for item in page_data:
                try:
                    await User.execute_query(User.insert(**item))
                except Exception as e:
                    logger.warning(e.__class__.__name__ + str(e.args))


async def page_task_division(page_from, page_to, max_levels, min_unit, level, loop):
    if page_to - page_from + 1 > min_unit and level < max_levels:
        middle = (page_from + page_to) // 2
        tasks = [
            page_task_division(page_from, middle, max_levels, min_unit, level + 1, loop),
            page_task_division(middle + 1, page_to, max_levels, min_unit, level + 1, loop)
        ]
        await asyncio.wait(tasks)
    else:
        await get_users(page_from, page_to)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(page_task_division(1, 100, 5, 5, 1, loop))
    loop.close()