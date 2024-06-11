from datetime import date

from pydantic import BaseModel, EmailStr


class DelayedEmail(BaseModel):
    body: str = ""
    subject: str = "Delayed email"
    email: EmailStr
    delivery_date: str
