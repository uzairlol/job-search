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
        payload = f"{prompt}\nProfile:\n{profile}\nCompany:\n{company}\nRoleHint:\n{role_hint or 'general'}"
        feedback = self.llm.polish(payload)
        return {
            "summary": feedback[:400],
            "skills": ["Python", "Machine Learning", "Research", "FastAPI"],
            "notes": feedback[:800],
        }
