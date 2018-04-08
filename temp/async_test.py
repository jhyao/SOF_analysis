import asyncio

async def task(n):
    print(f'task{n}...')
    await asyncio.sleep(n)
    print(f'task{n} end')

async def main(loop):
    asyncio.ensure_future(task(1))



if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main(loop))
    loop.close()