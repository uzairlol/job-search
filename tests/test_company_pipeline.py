from app.services.company_pipeline import CompanyPipelineService
from app.domain.models import Company


class InMemoryCompanyRepository:
    def __init__(self) -> None:
        self.items: list[Company] = []

    def save_many(self, companies: list[Company]) -> None:
        self.items.extend(companies)

    def list_all(self) -> list[Company]:
        return list(self.items)


class FakeProvider:
    def discover(self) -> list[Company]:
        return [
            Company(name="Test Co", remote_ok=True, source="fixture")
        ]


def test_company_pipeline_persists_discovered_companies() -> None:
    repository = InMemoryCompanyRepository()
    pipeline = CompanyPipelineService(provider=FakeProvider(), repository=repository)

    companies = pipeline.run()

    assert len(companies) == 1
    assert repository.list_all()[0].name == "Test Co"
