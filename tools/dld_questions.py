import asyncio

import data.config.config

from utils.date_transfer import *
from data.cdn.sof_cdn import QuestionsCDN

import logging

if __name__ == '__main__':
    result = QuestionsCDN.dld_pages_parallel(parallel_num=5, save=False, page=1, max_page=5)
    print(result)
    print(len(result))
