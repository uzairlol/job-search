from __future__ import annotations

import json
import smtplib
from email.message import EmailMessage
from pathlib import Path
from typing import Any

from app.core.settings import settings


class GmailSender:
    def __init__(self, host: str | None = None, port: int | None = None) -> None:
        self.host = host or settings.smtp_host
        self.port = port or settings.smtp_port
        self.user = settings.smtp_user
        self.password = settings.smtp_password

    def _build_message(self, recipient: str, subject: str, body: str, attachment_path: str | None = None) -> EmailMessage:
        message = EmailMessage()
        message["From"] = self.user
        message["To"] = recipient
        message["Subject"] = subject
        message.set_content(body)

        if attachment_path:
            attachment = Path(attachment_path)
            if attachment.exists():
                message.add_attachment(attachment.read_bytes(), maintype="application", subtype="pdf", filename=attachment.name)

        return message

    def send(self, recipient: str, subject: str, body: str, attachment_path: str | None = None) -> dict[str, Any]:
        if not self.user or not self.password:
            raise RuntimeError("SMTP credentials are not configured. Set SMTP_USER and SMTP_PASSWORD in your environment.")

        message = self._build_message(recipient=recipient, subject=subject, body=body, attachment_path=attachment_path)

        with smtplib.SMTP(self.host, self.port) as smtp:
            smtp.starttls()
            smtp.login(self.user, self.password)
            smtp.send_message(message)

        return {"recipient": recipient, "subject": subject, "sent": True}

    def schedule(
        self,
        recipient: str,
        subject: str,
        body: str,
        attachment_path: str | Path | None = None,
        output_dir: str | Path | None = None,
    ) -> dict[str, Any]:
        output_dir = Path(output_dir or Path("storage/scheduled_emails"))
        output_dir.mkdir(parents=True, exist_ok=True)

        attachment_path = str(attachment_path) if attachment_path is not None else None
        message = self._build_message(recipient=recipient, subject=subject, body=body, attachment_path=attachment_path)
        eml_path = output_dir / f"{Path(recipient).stem or 'email'}.eml"
        eml_path.write_bytes(message.as_bytes())

        manifest_path = output_dir / "manifest.json"
        manifest = []
        if manifest_path.exists():
            manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        manifest.append({
            "recipient": recipient,
            "subject": subject,
            "body": body,
            "attachment_path": attachment_path,
            "eml_path": str(eml_path),
            "status": "scheduled",
        })
        manifest_path.write_text(json.dumps(manifest, indent=2), encoding="utf-8")

        return {
            "recipient": recipient,
            "subject": subject,
            "body": body,
            "attachment_path": attachment_path,
            "eml_path": str(eml_path),
            "manifest_path": str(manifest_path),
            "scheduled": True,
            "status": "scheduled",
        }
