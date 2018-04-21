import asyncio

import data.config.config

from utils.date_transfer import *
from data.cdn.sof_cdn import QuestionsCDN

import logging

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(QuestionsCDN.dld_pages_async_parallel(
        page=296, sort='votes', min=0, parallel_num=5,
        fromdate=date_to_timestamp('2018-01-01'), todate=date_to_timestamp('2018-04-01')
    ))
    try:
        loop.close()
    except:
        pass
