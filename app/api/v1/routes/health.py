from fastapi import APIRouter

from app.core.config import settings
from app.services.discovery import CompanyDiscoveryService

router = APIRouter(prefix="/api/v1", tags=["health"])


@router.get("/health")
def health_check() -> dict[str, object]:
    return {"status": "ok", "app": settings.app_name, "environment": settings.environment}


@router.get("/companies")
def list_companies() -> list[dict[str, object]]:
    service = CompanyDiscoveryService()
    companies = service.discover()
    return [
        {
            "name": company.name,
            "website": company.website,
            "industry": company.industry,
            "country": company.country,
            "remote_ok": company.remote_ok,
            "source": company.source,
            "tags": company.tags,
        }
        for company in companies
    ]
