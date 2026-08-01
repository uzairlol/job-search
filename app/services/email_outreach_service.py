from __future__ import annotations

from typing import Any

from app.services.ollama_polisher import OllamaPolisher
from app.services.prompt_loader import PromptLoader


class EmailOutreachService:
    def __init__(self, prompt_loader: PromptLoader | None = None, llm: OllamaPolisher | None = None) -> None:
        self.prompt_loader = prompt_loader or PromptLoader()
        self.llm = llm or OllamaPolisher()

    def draft(self, company: dict[str, Any], profile: dict[str, Any], role_hint: str | None = None) -> dict[str, str]:
        prompt = self.prompt_loader.load("email_outreach.txt")
        profile_summary = profile.get("headline") or profile.get("summary") or "interested in this opportunity"
        profile_skills = ", ".join(profile.get("skills", [])[:5]) if profile.get("skills") else "relevant experience"
        payload = (
            f"{prompt}\nCompany:\n{company}\nProfileSummary:\n{profile_summary}\n"
            f"ProfileSkills:\n{profile_skills}\nRoleHint:\n{role_hint or 'general'}"
        )
        response = self.llm.polish(payload)
        subject = f"Re: {role_hint or 'opportunity'} at {company.get('name', 'your company')}"
        body = response[:1200]
        return {"subject": subject, "body": body}
