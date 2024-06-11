from datetime import datetime

from delayed_email.constants import DATE_FORMAT
from delayed_email.db.base import mongo_client
from delayed_email.settings import settings
from delayed_email.worker.rabbitmq import get_rabbitmq_client


async def producer():
    current_date = datetime.now()
    date_string = current_date.strftime(DATE_FORMAT)
    print("##############")
    print(date_string)
    async with mongo_client() as client:
        db = client.get_database(settings.mongodb.db_name)
        result = db.email_collection.find({"delivery_date": date_string})
        result = await result.to_list(length=100)
    # send to rabbitMQ
    messages = []
    for i in result:
        i.pop("_id", "")
        messages.append(i)
    print(messages)
    rabbitmq_client = get_rabbitmq_client()
    await rabbitmq_client.publish(settings.rabbitmq.routing_key, messages)
    await rabbitmq_client.disconnect()
