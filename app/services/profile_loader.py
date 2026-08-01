from __future__ import annotations

import json
import re
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

        combined = "\n".join(raw_context).strip()
        name = self._extract_name(combined)
        email = self._extract_email(combined)
        location = self._extract_location(combined)
        summary = self._extract_summary(raw_context)
        skills = self._extract_skills(raw_context)
        headline = self._extract_headline(summary, skills)

        return Profile(
            name=name or "Your Name",
            email=email or "you@example.com",
            phone=None,
            location=location or "Remote",
            headline=headline,
            summary=summary,
            skills=skills,
            experience=[],
            projects=[],
            education=[],
            certifications=[],
            raw_context=raw_context,
        )

    def _extract_name(self, combined: str) -> str | None:
        patterns = [
            r"Name:\s*(.+)",
            r"^#\s*(.+)$",
            r"^([A-Z][a-z]+(?:\s+[A-Z][a-z]+)+)$",
        ]
        for pattern in patterns:
            match = re.search(pattern, combined, re.MULTILINE)
            if match:
                return match.group(1).strip()
        return None

    def _extract_email(self, combined: str) -> str | None:
        match = re.search(r"([A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,})", combined)
        return match.group(1).strip() if match else None

    def _extract_location(self, combined: str) -> str | None:
        match = re.search(r"Location:\s*(.+)", combined, re.IGNORECASE)
        if match:
            return match.group(1).strip()
        return None

    def _extract_summary(self, raw_context: list[str]) -> str:
        combined = "\n".join(raw_context).strip()
        if not combined:
            return "Applied engineer with strong software and research experience."
        first_line = next((line.strip() for line in combined.splitlines() if line.strip()), "")
        if first_line.startswith("#"):
            first_line = first_line.lstrip("#").strip()
        return first_line[:280] or "Applied engineer with strong software and research experience."

    def _extract_headline(self, summary: str, skills: list[str]) -> str:
        skill_text = ", ".join(skills[:4])
        return f"Applied professional focused on {skill_text}" if skill_text else summary

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
            "aws",
            "azure",
            "kubernetes",
            "llm",
            "langchain",
        ]
        found = [skill for skill in candidates if skill in combined]
        if not found:
            return ["Python", "Machine Learning", "Research"]
        return [skill.title() for skill in found]
