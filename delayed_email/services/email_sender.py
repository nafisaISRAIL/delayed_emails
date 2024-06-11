import smtplib

from delayed_email.settings import settings


class EmailSender:
    @staticmethod
    async def send_email(email_data: dict) -> None:
        from_email = settings.smtp.username
        to_email = email_data.get("email")
        subject = email_data["subject"]
        body = email_data["body"]
        message = f"Subject: {subject}\n\n{body}"

        with smtplib.SMTP(settings.smtp.server, settings.smtp.port) as smtp:
            smtp.starttls()
            smtp.login(settings.smtp.username, settings.smtp.password)
            smtp.sendmail(from_email, to_email, message)
