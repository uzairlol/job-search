from __future__ import annotations

import smtplib
from email.message import EmailMessage
from typing import Any

from app.core.settings import settings


class GmailSender:
    def __init__(self, host: str | None = None, port: int | None = None) -> None:
        self.host = host or settings.smtp_host
        self.port = port or settings.smtp_port
        self.user = settings.smtp_user
        self.password = settings.smtp_password

    def send(self, recipient: str, subject: str, body: str) -> dict[str, Any]:
        if not self.user or not self.password:
            raise RuntimeError("SMTP credentials are not configured. Set SMTP_USER and SMTP_PASSWORD in your environment.")

        message = EmailMessage()
        message["From"] = self.user
        message["To"] = recipient
        message["Subject"] = subject
        message.set_content(body)

        with smtplib.SMTP(self.host, self.port) as smtp:
            smtp.starttls()
            smtp.login(self.user, self.password)
            smtp.send_message(message)

        return {"recipient": recipient, "subject": subject, "sent": True}
