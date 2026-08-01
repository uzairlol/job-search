from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class DraftEmail:
    subject: str
    body: str


class EmailBuilder:
    def build(self, company: dict[str, object], profile: dict[str, object], target_role: str) -> DraftEmail:
        company_name = str(company.get("name", "the company"))
        body = (
            f"Hi {company_name} recruiting team,\n\n"
            f"I’m reaching out because I’m very interested in the {target_role} opportunity at {company_name}. "
            f"I’ve tailored my background around remote, research-driven, and production-oriented ML work, and I would be excited to explore whether my experience could be a fit.\n\n"
            f"My background spans applied ML, software engineering, and delivery of reliable systems in production. "
            f"I’d welcome the opportunity to discuss how I could contribute to {company_name}.\n\n"
            f"Best regards,\n{profile.get('name', 'Your Name')}"
        )
        subject = f"Re: {target_role} opportunity at {company_name}"
        return DraftEmail(subject=subject, body=body)
