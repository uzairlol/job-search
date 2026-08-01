from __future__ import annotations

from pathlib import Path

from app.core.settings import settings


class PromptLoader:
    def __init__(self, prompt_dir: str | Path | None = None) -> None:
        self.prompt_dir = Path(prompt_dir or settings.prompt_dir)

    def load(self, prompt_name: str) -> str:
        path = self.prompt_dir / prompt_name
        if not path.exists():
            raise FileNotFoundError(f"Prompt file not found: {path}")
        return path.read_text(encoding="utf-8")
