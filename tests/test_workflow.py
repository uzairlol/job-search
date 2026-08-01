import json
from pathlib import Path

from app.services.discovery import CompanyDiscoveryService
from app.services.email_builder import EmailBuilder
from app.services.ollama_polisher import OllamaPolisher
from app.services.resume_builder import ResumeBuilder


def test_discovery_ranks_remote_friendly_companies() -> None:
    service = CompanyDiscoveryService()
    opportunities = service.discover(target_role="Machine Learning Engineer")

    assert opportunities
    assert opportunities[0].score >= opportunities[-1].score
    assert any(company.remote_ok for company in opportunities)


def test_resume_builder_creates_latex_resume() -> None:
    profile = {
        "name": "Ada Lovelace",
        "email": "ada@example.com",
        "phone": "+1-555-0100",
        "location": "Remote",
        "summary": "Applied ML engineer with strong Python and research experience.",
        "skills": ["Python", "PyTorch", "FastAPI", "PostgreSQL"],
        "experience": [
            {
                "title": "ML Engineer",
                "company": "Open Research Lab",
                "dates": "2022-2024",
                "bullets": [
                    "Built retrieval systems for research workflows.",
                    "Delivered production-ready ML services in Python.",
                ],
            }
        ],
        "projects": [
            {
                "name": "Autonomous Research Agent",
                "description": "Designed a multi-step system for document understanding.",
            }
        ],
    }
    builder = ResumeBuilder()
    latex = builder.build(profile=profile, target_role="Machine Learning Engineer")

    assert "\\documentclass" in latex
    assert "Machine Learning Engineer" in latex
    assert "Applied ML engineer" in latex


def test_email_builder_creates_personalized_outreach() -> None:
    company = {"name": "Northstar Labs", "website": "https://northstar.example", "country": "Remote"}
    profile = {"name": "Ada Lovelace", "headline": "Applied ML engineer"}
    builder = EmailBuilder()
    email = builder.build(company=company, profile=profile, target_role="Machine Learning Engineer")

    assert email.subject.startswith("Re:") or "Northstar Labs" in email.subject
    assert "Northstar Labs" in email.body
    assert "Machine Learning Engineer" in email.body


def test_ollama_polisher_falls_back_to_original_text(monkeypatch) -> None:
    def fake_run(*_args, **_kwargs) -> object:
        raise FileNotFoundError

    monkeypatch.setattr("app.services.ollama_polisher.subprocess.run", fake_run)
    polisher = OllamaPolisher()

    assert polisher.polish("hello") == "hello"
