from pathlib import Path

from app.integrations.email.gmail_sender import GmailSender
from app.services.review_service import ReviewService


class FakeLLM:
    def __init__(self, response: str) -> None:
        self.response = response

    def polish(self, text: str) -> str:
        return self.response


def test_review_service_refines_text() -> None:
    service = ReviewService(llm=FakeLLM("Improved draft"))

    result = service.review("Basic draft", "email", {"company": "Northstar Labs"})

    assert result == "Improved draft"


def test_gmail_sender_schedules_message_with_attachment(tmp_path: Path) -> None:
    sender = GmailSender()
    attachment = tmp_path / "resume.pdf"
    attachment.write_bytes(b"%PDF-1.4")

    result = sender.schedule(
        recipient="candidate@example.com",
        subject="Re: Opportunity",
        body="Hello from the workflow",
        attachment_path=attachment,
        output_dir=tmp_path,
    )

    assert result["status"] == "scheduled"
    assert result["scheduled"] is True
    assert Path(result["eml_path"]).exists()
    assert Path(result["manifest_path"]).exists()
    assert result["attachment_path"] == str(attachment)
