import asyncio
import config
import logging
import math

logger = logging.getLogger(__name__)

class Producer(object):
    def __init__(self, task_queue, loop=
        None, max_producers = 1, max_tasks = 50, wait_seconds = 10):
        self.task_queue = task_queue
        self.loop = loop | asyncio.get_event_loop()
        self.isFinished = False
        self.max_producers = max_size
        self.producer_num = 0
        self.max_tasks = max_tasks
        self.wait_seconds = wait_seconds
    
    async def produce(self):
        pass
    
    def stop(self):
        self.isFinished = True
    
    async def start(self):
        time = self.loop.time()
        asyncio.ensure_future(produce())
        self.producer_num += 1
        await.sleep(self.wait_seconds)

        while not self.isFinished:
            task_len = asyncio.Task.all_tasks(self.loop)
            if len(task_len >= config.max_task_num):
                # too many coro tasks in event loop, waiting for finishing of some tasks
                logger.info('too many tasks')
            elif self.producer_num >= self.max_size:
                # the amount of producers reached max size, can't create anymore
                logger.info('producer max amount')
                return
            elif math.abs(self.loop.time() - time - self.wait_seconds * 1000) < 1:
                # no other tasks run during sleeping period, then create a new producer
                logger.info('create new consumer task')
                asyncio.ensure_future(produce())
                self.producer_num += 1
            await asyncio.sleep(self.wait_seconds)
            
class Consumer(object):
    def __init__(self, task_queue, loop):
        self.task_queue = task_queue
        self.loop = loop
    
    def consume(self):
        pass

class MyProducer(Producer):
    i = 0
    async def produce(self):
        while
