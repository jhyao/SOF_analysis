import asyncio

async def task():
    print(f'task...')
    await asyncio.sleep(1)
    return [1]

async def main(loop):
    task_list = [task() for i in range(5)]
    tasks = await asyncio.wait(task_list)
    result = [t.result() for t in tasks[0]]
    print(result)
    return result



if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main(loop))
    loop.close()