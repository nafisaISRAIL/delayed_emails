from contextlib import asynccontextmanager

from motor.motor_asyncio import AsyncIOMotorClient

from delayed_email.settings import settings


@asynccontextmanager
async def mongo_client():
    uri = settings.mongodb.uri
    client = AsyncIOMotorClient(uri)
    try:
        await client.admin.command("ping")
        yield client
    except Exception:
        raise
    finally:
        client.close()
