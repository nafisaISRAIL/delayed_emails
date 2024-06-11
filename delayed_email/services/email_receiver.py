import json

from delayed_email.containers import DelayedEmail
from delayed_email.db.base import mongo_client
from delayed_email.settings import settings


class DelayedEmailService:
    @staticmethod
    async def delay_email(email: DelayedEmail) -> DelayedEmail:
        async with mongo_client() as client:
            try:
                db = client.get_database(settings.mongodb.db_name)
                d = json.loads(email.model_dump_json())
                await db.email_collection.insert_one(d)
            except Exception as exc:
                raise exc
        return email

    @staticmethod
    async def get_delayed_emails() -> [DelayedEmail]:
        async with mongo_client() as client:
            try:
                db = client.get_database(settings.mongodb.db_name)
                result = db.email_collection.find({})
                result = await result.to_list(length=100)
                return [DelayedEmail(**doc) for doc in result]
            except Exception as e:
                raise e
