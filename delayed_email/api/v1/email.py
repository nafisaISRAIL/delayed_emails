from fastapi import APIRouter

from delayed_email.containers import DelayedEmail
from delayed_email.services.email_receiver import DelayedEmailService

email_router = APIRouter()


@email_router.post(
    "/v1/emails",
)
async def delay_email(email: DelayedEmail) -> DelayedEmail:
    return await DelayedEmailService.delay_email(email)


@email_router.get("/v1/emails")
async def delay_emails() -> list[DelayedEmail]:
    return await DelayedEmailService.get_delayed_emails()
