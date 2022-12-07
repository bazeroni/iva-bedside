import asyncio

async def one():
    print("one start")
    await asyncio.sleep(5)
    print("one done")

async def two():
    print("two start")
    await asyncio.sleep(5)
    print("two done")
    
loop = asyncio.get_event_loop()
asyncio.set_event_loop(loop)
loop.run_until_complete(asyncio.gather(one(), two()))