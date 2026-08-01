from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from app.domain.models import Profile


class ProfileLoader:
    def __init__(self, profile_dir: str | Path | None = None) -> None:
        self.profile_dir = Path(profile_dir or "user_profile")

    def load(self) -> Profile:
        self.profile_dir.mkdir(parents=True, exist_ok=True)

        if (self.profile_dir / "profile.json").exists():
            payload = json.loads((self.profile_dir / "profile.json").read_text(encoding="utf-8"))
            return Profile(**payload)

        raw_context: list[str] = []
        for file_path in sorted(self.profile_dir.glob("*.md")):
            raw_context.append(file_path.read_text(encoding="utf-8"))
        for file_path in sorted(self.profile_dir.glob("*.txt")):
            raw_context.append(file_path.read_text(encoding="utf-8"))

        summary = self._extract_summary(raw_context)
        skills = self._extract_skills(raw_context)
        headline = "Applied ML engineer focused on research and deployment"

        return Profile(
            name="Your Name",
            email="you@example.com",
            phone=None,
            location="Remote",
            headline=headline,
            summary=summary,
            skills=skills,
            experience=[],
            projects=[],
            education=[],
            certifications=[],
            raw_context=raw_context,
        )

    def _extract_summary(self, raw_context: list[str]) -> str:
        combined = "\n".join(raw_context).strip()
        if not combined:
            return "Applied engineer with strong software and research experience."
        return combined.splitlines()[0][:280]

    def _extract_skills(self, raw_context: list[str]) -> list[str]:
        combined = "\n".join(raw_context).lower()
        candidates = [
            "python",
            "pytorch",
            "fastapi",
            "sqlalchemy",
            "postgresql",
            "docker",
            "linux",
            "machine learning",
            "research",
            "nlp",
            "redis",
            "pytest",
        ]
        found = [skill for skill in candidates if skill in combined]
        if not found:
            return ["Python", "Machine Learning", "Research"]
        return [skill.title() for skill in found]
