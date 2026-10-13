import asyncio
import traceback


async def consume(process_id: str, queue: asyncio.Queue):
    try:
        while True:
            val = await queue.get()
            await asyncio.sleep(0)

            print(process_id, val)

            if val == 30:
                queue.put_nowait(val + 1000)

            queue.task_done()

    except Exception as e:
        if not isinstance(e, asyncio.exceptions.CancelledError):
            traceback.print_exc()


async def main():
    q = asyncio.Queue()

    for i in range(100):
        print(f"Putting {i * 10} into the queue")
        q.put_nowait(i * 10)

    consumers = [asyncio.create_task(consume(f"Process {i}", q)) for i in range(3)]

    await q.join()

    for c in consumers:
        c.cancel()


asyncio.run(main())
