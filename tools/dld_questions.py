import asyncio

from data.cdn.sof_cdn import QuestionsCDN

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(QuestionsCDN.dld_pages_async_parallel(page=70, fromdate=1488326400, todate=1491004800, sort='votes', min=0))
    try:
        loop.close()
    except:
        pass
