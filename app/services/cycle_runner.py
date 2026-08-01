from __future__ import annotations

import subprocess
from pathlib import Path
from typing import Any

from app.core.settings import settings
from app.infrastructure.database.repositories import CompanyRepository, CycleRunRepository, EmailDraftRepository
from app.infrastructure.database.session import get_session
from app.services.artifact_store import ArtifactStore
from app.services.company_discovery_engine import CompanyDiscoveryEngine
from app.services.database_guard import DatabaseGuard
from app.services.email_outreach_service import EmailOutreachService
from app.services.profile_ingestion import ProfileIngestionService
from app.services.profile_loader import ProfileLoader
from app.services.resume_builder import ResumeBuilder
from app.services.resume_tailoring_service import ResumeTailoringService


class CycleRunner:
    def __init__(self, profile_dir: str | Path | None = None, artifact_root: str | Path | None = None) -> None:
        self.profile_dir = Path(profile_dir or settings.profile_dir)
        self.artifact_store = ArtifactStore(root=artifact_root or settings.artifact_root)
        self.profile_loader = ProfileLoader(profile_dir=self.profile_dir)
        self.discovery_engine = CompanyDiscoveryEngine()
        self.resume_tailoring = ResumeTailoringService()
        self.email_outreach = EmailOutreachService()
        self.resume_builder = ResumeBuilder()
        self.profile_ingestion = ProfileIngestionService(profile_dir=self.profile_dir)
        self.database_guard = DatabaseGuard()

    def run_once(self, focus_terms: str | None = None, company_limit: int = 3) -> dict[str, Any]:
        self.profile_ingestion.ingest()
        profile = self.profile_loader.load()
        focus_terms = focus_terms or settings.default_company_focus
        companies = self.discovery_engine.discover(focus_terms=focus_terms)[:company_limit]

        run_dir = self.artifact_store.make_run_dir()
        run_dir.mkdir(parents=True, exist_ok=True)

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
            target_role="Remote AI/ML opportunity",
            output_path=run_dir / "resume.tex",
        )
        pdf_path = self._compile_latex(resume_path)

        session = self.database_guard.safe_session()
        if session is not None:
            with session:
                company_repo = CompanyRepository(session)
                company_repo.upsert_many([
                    {
                        "name": company.name,
                        "website": company.website,
                        "industry": company.industry,
                        "country": company.country,
                        "remote_ok": company.remote_ok,
                        "score": int(company.score),
                        "source": company.source,
                        "tags": company.tags,
                        "summary": company.rationale,
                    }
                    for company in companies
                ])

                email_repo = EmailDraftRepository(session)
                for company in companies:
                    draft = self.email_outreach.draft(
                        company={"name": company.name, "website": company.website, "country": company.country},
                        profile={"name": profile.name, "headline": profile.headline},
                        role_hint="Remote AI/ML opportunity",
                    )
                    email_repo.save(company.name, draft["subject"], draft["body"])

                cycle_repo = CycleRunRepository(session)
                cycle_repo.save(profile.name, focus_terms, str(run_dir))
        else:
            print("[database] Postgres is unavailable; continuing without persistence.")

        return {
            "profile": profile.name,
            "focus_terms": focus_terms,
            "companies": [company.name for company in companies],
            "resume_path": str(resume_path),
            "pdf_path": str(pdf_path) if pdf_path else None,
            "artifacts_dir": str(run_dir),
        }

    def _compile_latex(self, tex_path: Path) -> Path | None:
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
        try:
            result = subprocess.run(command, capture_output=True, text=True, cwd=output_dir.as_posix(), encoding="utf-8", errors="replace")
        except FileNotFoundError:
            print("[tex] pdflatex is not available; skipping PDF compilation")
            return None

        if pdf_path.exists():
            print(f"[tex] compiled PDF to {pdf_path}")
            return pdf_path

        if result.returncode != 0:
            print(result.stdout)
            print(result.stderr)
            print("[tex] pdflatex compilation failed; continuing with LaTeX output")
            return None

        return None
