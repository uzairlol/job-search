from __future__ import annotations

from typing import Any

from app.services.ollama_polisher import OllamaPolisher


class ReviewService:
    def __init__(self, llm: OllamaPolisher | None = None) -> None:
        self.llm = llm or OllamaPolisher()

    def review(self, draft: str, context: str, metadata: dict[str, Any] | None = None) -> str:
        metadata = metadata or {}
        prompt = (
            f"You are reviewing a {context} draft for an outreach workflow. "
            f"Improve clarity, specificity, and persuasiveness while preserving the core meaning. "
            f"Return only the improved draft.\n"
            f"Context: {metadata}\n"
            f"Draft:\n{draft}"
        )
        reviewed = self.llm.polish(prompt)
        return reviewed.strip() or draft
