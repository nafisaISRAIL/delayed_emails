import asyncio
import json

from aio_pika.abc import AbstractIncomingMessage

from delayed_email.services.email_sender import EmailSender
from delayed_email.worker.rabbitmq import get_rabbitmq_client


async def on_message(message: AbstractIncomingMessage):
    txt = message.body.decode("utf-8")
    await EmailSender.send_email(json.loads(txt))


async def main(_):
    rabbitmq_client = get_rabbitmq_client()
    async with rabbitmq_client.channel_pool.acquire() as channel:
        await channel.set_qos(5)
        queue = await channel.declare_queue("email_sender", auto_delete=False)
        async with queue.iterator() as queue_iter:
            async for message in queue_iter:
                print("go message")
                await on_message(message)
                # txt = message.body.decode("utf-8")
                # msg = json.loads(txt)
                # print(msg)
                await message.ack()


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.create_task(main(loop))
    loop.run_forever()
