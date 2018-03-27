from .models.sof_models import Post
import asyncio
import json

async def async_test():
    post = await Post.create_from_json(json.dumps({'post_id':4, 'post_type':'answer', 'link':'sfsd'}))
    print(post)

loop = asyncio.get_event_loop()
loop.run_until_complete(async_test())
loop.close()
