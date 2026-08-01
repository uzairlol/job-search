from __future__ import annotations

import subprocess
from pathlib import Path
from typing import Any

from app.services.discovery import CompanyDiscoveryService
from app.services.email_builder import DraftEmail, EmailBuilder
from app.services.ollama_polisher import OllamaPolisher
from app.services.outbox import OutboxWriter
from app.services.profile_loader import ProfileLoader
from app.services.resume_builder import ResumeBuilder


class LocalJobWorkflow:
    def __init__(self, profile_dir: str | Path | None = None) -> None:
        self.profile_dir = profile_dir
        self.discovery = CompanyDiscoveryService()
        self.profile_loader = ProfileLoader(profile_dir=profile_dir)
        self.resume_builder = ResumeBuilder()
        self.email_builder = EmailBuilder()
        self.polisher = OllamaPolisher()
        self.outbox = OutboxWriter()

    def run(self, target_role: str = "Machine Learning Engineer", company_limit: int = 3) -> dict[str, Any]:
        profile = self.profile_loader.load()
        opportunities = self.discovery.discover(target_role=target_role)[:company_limit]
        print(f"[workflow] discovered {len(opportunities)} remote-friendly opportunities")

        resume_path = self.resume_builder.write(
            profile={
                "name": profile.name,
                "email": profile.email,
                "phone": profile.phone,
                "location": profile.location,
                "summary": profile.summary,
                "skills": profile.skills,
                "experience": profile.experience,
                "projects": profile.projects,
            },
            target_role=target_role,
            output_path="artifacts/resume.tex",
        )
        print(f"[workflow] wrote resume LaTeX to {resume_path}")

        self._compile_latex(resume_path)

        drafts: list[tuple[dict[str, object], DraftEmail]] = []
        for opportunity in opportunities:
            email = self.email_builder.build(
                company={
                    "name": opportunity.name,
                    "website": opportunity.website,
                    "country": opportunity.country,
                },
                profile={"name": profile.name},
                target_role=target_role,
            )
            polished_body = self.polisher.polish(email.body)
            drafts.append(({"name": opportunity.name}, DraftEmail(subject=email.subject, body=polished_body)))
            self.outbox.write(opportunity.name, email.subject, polished_body)
            print(f"[workflow] draft email for {opportunity.name}: {email.subject}")
            print(f"[workflow] saved outreach draft to artifacts/outbox/{opportunity.name.lower().replace(' ', '_')}.json")

        return {
            "profile": profile.name,
            "target_role": target_role,
            "opportunities": [opportunity.name for opportunity in opportunities],
            "resume_path": str(resume_path),
            "pdf_path": "artifacts/resume.pdf",
            "emails": [{"company": company["name"], "subject": email.subject} for company, email in drafts],
        }

    def _compile_latex(self, tex_path: Path) -> None:
        tex_path = tex_path.resolve()
        output_dir = tex_path.parent.resolve()
        pdf_path = output_dir / tex_path.with_suffix(".pdf").name
        command = [
            "pdflatex",
            "-interaction=nonstopmode",
            "-output-directory",
            output_dir.as_posix(),
            tex_path.as_posix(),
        ]
        result = subprocess.run(command, capture_output=True, text=True, cwd=output_dir.as_posix())
        if result.returncode != 0:
            print(result.stdout)
            print(result.stderr)
            raise RuntimeError("pdflatex compile failed")
        if pdf_path.exists():
            print(f"[workflow] compiled PDF to {pdf_path}")
