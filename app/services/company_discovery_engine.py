from __future__ import annotations

from dataclasses import dataclass
from typing import List

from app.core.settings import settings
from app.services.ollama_polisher import OllamaPolisher
from app.services.prompt_loader import PromptLoader


REAL_COMPANY_SEEDS = [
    {
        "name": "OpenAI",
        "website": "https://openai.com",
        "industry": "AI",
        "country": "Remote",
        "remote_ok": True,
        "tags": ["ai", "remote", "research"],
        "score": 98.0,
    },
    {
        "name": "Anthropic",
        "website": "https://www.anthropic.com",
        "industry": "AI",
        "country": "Remote",
        "remote_ok": True,
        "tags": ["ai", "remote", "ml"],
        "score": 96.0,
    },
    {
        "name": "Databricks",
        "website": "https://www.databricks.com",
        "industry": "Data",
        "country": "Remote",
        "remote_ok": True,
        "tags": ["data", "remote", "engineering"],
        "score": 94.0,
    },
    {
        "name": "GitLab",
        "website": "https://about.gitlab.com",
        "industry": "Developer Tools",
        "country": "Remote",
        "remote_ok": True,
        "tags": ["devtools", "remote", "platform"],
        "score": 92.0,
    },
    {
        "name": "Notion",
        "website": "https://www.notion.so",
        "industry": "Productivity",
        "country": "Remote",
        "remote_ok": True,
        "tags": ["product", "remote", "ai"],
        "score": 90.0,
    },
]


@dataclass(slots=True)
class CompanyTarget:
    name: str
    website: str | None
    industry: str | None
    country: str | None
    remote_ok: bool
    score: float
    source: str
    tags: List[str]
    rationale: str | None = None


class CompanyDiscoveryEngine:
    def __init__(self, prompt_loader: PromptLoader | None = None, llm: OllamaPolisher | None = None) -> None:
        self.prompt_loader = prompt_loader or PromptLoader()
        self.llm = llm or OllamaPolisher(model=settings.ollama_model)

    def discover(self, focus_terms: str = "remote ai ml research") -> list[CompanyTarget]:
        prompt = self.prompt_loader.load("company_discovery.txt")
        seed = []
        for payload in REAL_COMPANY_SEEDS:
            seed.append(
                CompanyTarget(
                    name=payload["name"],
                    website=payload["website"],
                    industry=payload["industry"],
                    country=payload["country"],
                    remote_ok=payload["remote_ok"],
                    score=payload["score"],
                    source="seed",
                    tags=payload["tags"],
                )
            )

        scored = []
        for company in seed:
            focus_hit = sum(1 for term in focus_terms.lower().split() if term in " ".join(company.tags + [company.industry or ""]).lower())
            remote_bonus = 8 if company.remote_ok else 0
            score = company.score + focus_hit * 3 + remote_bonus
            rationale = self._run_llm(prompt, company.name, focus_terms, score)
            scored.append(
                CompanyTarget(
                    name=company.name,
                    website=company.website,
                    industry=company.industry,
                    country=company.country,
                    remote_ok=company.remote_ok,
                    score=score,
                    source=company.source,
                    tags=company.tags,
                    rationale=rationale,
                )
            )

        scored.sort(key=lambda item: item.score, reverse=True)
        return scored

    def _run_llm(self, prompt: str, company_name: str, focus_terms: str, score: float) -> str:
        payload = f"{prompt}\nCompany: {company_name}\nFocus terms: {focus_terms}\nScore: {score}"
        response = self.llm.polish(payload)
        return response[:280]
