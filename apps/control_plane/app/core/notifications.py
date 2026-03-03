import smtplib
from email.mime.text import MIMEText
import httpx
from apps.control_plane.app.core.config import settings

class Notifier:
    async def telegram_send(self, text: str) -> None:
        if not (settings.TELEGRAM_BOT_TOKEN and settings.TELEGRAM_CHAT_ID):
            return
        url = f"https://api.telegram.org/bot{settings.TELEGRAM_BOT_TOKEN}/sendMessage"
        async with httpx.AsyncClient(timeout=10) as client:
            await client.post(url, json={"chat_id": settings.TELEGRAM_CHAT_ID, "text": text})

    def email_send(self, subject: str, body: str) -> None:
        if not (settings.SMTP_HOST and settings.SMTP_USER and settings.SMTP_PASS and settings.SMTP_FROM and settings.EMAIL_TO):
            return

        msg = MIMEText(body, "plain", "utf-8")
        msg["Subject"] = subject
        msg["From"] = settings.SMTP_FROM
        msg["To"] = settings.EMAIL_TO

        with smtplib.SMTP(settings.SMTP_HOST, settings.SMTP_PORT, timeout=20) as s:
            s.starttls()
            s.login(settings.SMTP_USER, settings.SMTP_PASS)
            s.sendmail(settings.SMTP_FROM, [settings.EMAIL_TO], msg.as_string())

notifier = Notifier()