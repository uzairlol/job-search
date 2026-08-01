from app.services.company_discovery_engine import CompanyDiscoveryEngine
from app.services.email_outreach_service import EmailOutreachService
from app.services.profile_ingestion import ProfileIngestionService
from app.services.resume_tailoring_service import ResumeTailoringService


def test_company_discovery_engine_returns_ranked_targets(tmp_path) -> None:
    engine = CompanyDiscoveryEngine()
    results = engine.discover(focus_terms="remote ai ml")
    assert results
    assert results[0].score >= results[-1].score


def test_email_outreach_service_returns_subject_and_body() -> None:
    service = EmailOutreachService()
    draft = service.draft({"name": "Northstar Labs"}, {"name": "Ada"}, role_hint="Remote ML Engineer")
    assert draft["subject"]
    assert draft["body"]


def test_resume_tailoring_service_returns_structured_guidance() -> None:
    service = ResumeTailoringService()
    result = service.tailor({"name": "Ada"}, {"name": "Northstar Labs"}, role_hint="Remote ML Engineer")
    assert "summary" in result
    assert "skills" in result


def test_profile_ingestion_reads_profile_dir(tmp_path) -> None:
    profile_dir = tmp_path / "profile"
    profile_dir.mkdir()
    (profile_dir / "notes.md").write_text("hello world", encoding="utf-8")
    service = ProfileIngestionService(profile_dir=profile_dir)
    documents = service.ingest()
    assert documents[0]["name"] == "notes.md"
