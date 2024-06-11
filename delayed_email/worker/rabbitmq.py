import json

import aio_pika
from aio_pika import Message, connect_robust
from aio_pika.abc import (
    AbstractChannel,
    AbstractRobustChannel,
    AbstractRobustConnection,
)
from aio_pika.pool import Pool

from delayed_email.settings import settings


class RabbitmqClient:
    def __init__(self, host: str, username: str, password: str) -> None:
        self.host = host
        self.username = username
        self.password = password
        self.connection_pool: Pool[aio_pika.RobustConnection] = Pool(
            self.get_connection,
        )
        self.channel_pool: Pool[aio_pika.RobustChannel] = Pool(
            self.get_channel,
        )

    async def get_connection(self) -> AbstractRobustConnection:
        return await aio_pika.connect_robust(
            host=self.host, login=self.username, password=self.password
        )

    async def get_channel(self) -> AbstractChannel:
        async with self.connection_pool.acquire() as connection:
            channel = await connection.channel()
            return channel

    async def disconnect(self) -> None:
        await self.channel_pool.close()
        await self.connection_pool.close()

    async def publish(self, queue_name: str, messages: list[dict]):
        async with self.channel_pool.acquire() as channel:
            for message in messages:
                send_message = Message(body=json.dumps(message).encode())
                await channel.default_exchange.publish(
                    send_message,
                    routing_key=queue_name,
                )


def get_rabbitmq_client() -> RabbitmqClient:
    return RabbitmqClient(
        username=settings.rabbitmq.username,
        password=settings.rabbitmq.password,
        host=settings.rabbitmq.host,
    )
