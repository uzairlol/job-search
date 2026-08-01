from __future__ import annotations

from typing import Any

from sqlalchemy.orm import Session

from app.infrastructure.database.models import CompanyRecord, CycleRunRecord, EmailDraftRecord, ProfileDocument


class CompanyRepository:
    def __init__(self, session: Session) -> None:
        self.session = session

    def upsert_many(self, companies: list[dict[str, Any]]) -> None:
        for payload in companies:
            record = self.session.query(CompanyRecord).filter(CompanyRecord.name == payload["name"]).first()
            if record is None:
                record = CompanyRecord(name=payload["name"])
            record.website = payload.get("website")
            record.industry = payload.get("industry")
            record.country = payload.get("country")
            record.remote_ok = payload.get("remote_ok", False)
            record.score = payload.get("score", 0)
            record.source = payload.get("source")
            record.tags = ",".join(payload.get("tags", []))
            record.summary = payload.get("summary")
            self.session.add(record)
        self.session.commit()


class ProfileRepository:
    def __init__(self, session: Session) -> None:
        self.session = session

    def store_document(self, document_name: str, content: str) -> None:
        self.session.add(ProfileDocument(document_name=document_name, content=content))
        self.session.commit()


class EmailDraftRepository:
    def __init__(self, session: Session) -> None:
        self.session = session

    def save(self, company_name: str, subject: str, body: str, status: str = "draft") -> None:
        self.session.add(EmailDraftRecord(company_name=company_name, subject=subject, body=body, status=status))
        self.session.commit()


class CycleRunRepository:
    def __init__(self, session: Session) -> None:
        self.session = session

    def save(self, profile_name: str, focus_terms: str, artifact_dir: str | None) -> None:
        self.session.add(CycleRunRecord(profile_name=profile_name, focus_terms=focus_terms, artifact_dir=artifact_dir))
        self.session.commit()
