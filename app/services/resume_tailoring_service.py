from __future__ import annotations

from typing import Any

from app.services.ollama_polisher import OllamaPolisher
from app.services.prompt_loader import PromptLoader


class ResumeTailoringService:
    def __init__(self, prompt_loader: PromptLoader | None = None, llm: OllamaPolisher | None = None) -> None:
        self.prompt_loader = prompt_loader or PromptLoader()
        self.llm = llm or OllamaPolisher()

    def tailor(self, profile: dict[str, Any], company: dict[str, Any], role_hint: str | None = None) -> dict[str, Any]:
        prompt = self.prompt_loader.load("resume_tailoring.txt")
        profile_skills = profile.get("skills", []) or []
        company_name = company.get("name", "the company")
        company_industry = company.get("industry") or "the relevant field"
        company_tags = company.get("tags", []) or []
        suggested_skills = list(profile_skills)
        for tag in company_tags:
            if tag not in suggested_skills:
                suggested_skills.append(tag.title())
        suggested_skills = suggested_skills[:8]
        payload = (
            f"{prompt}\nProfile:\n{profile}\nCompany:\n{company}\n"
            f"RoleHint:\n{role_hint or 'general'}\nFocus:\n{company_name} in {company_industry}"
        )
        feedback = self.llm.polish(payload)
        return {
            "summary": feedback[:400],
            "skills": suggested_skills,
            "notes": feedback[:800],
        }
