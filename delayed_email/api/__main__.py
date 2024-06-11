import asyncio

from fastapi import FastAPI
from fastapi_utilities import repeat_at
from uvicorn import Config, Server

from delayed_email.api.health import health_router
from delayed_email.api.v1.email import email_router
from delayed_email.services.selector import producer

app = FastAPI(title="receiver", description="Delay email sending")

app.include_router(email_router)
app.include_router(health_router)


@app.on_event("startup")
@repeat_at(cron="* * * * *")
async def start_cron_email_selector():
    await producer()


async def start_app() -> None:
    server = Server(
        Config("__main__:app", host="0.0.0.0", port=8000),
    )
    await server.serve()


if __name__ == "__main__":
    asyncio.run(start_app())
