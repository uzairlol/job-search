from app.domain.interfaces import CompanyDiscoveryProvider, CompanyRepository
from app.domain.models import Company


class CompanyPipelineService:
    def __init__(self, provider: CompanyDiscoveryProvider, repository: CompanyRepository) -> None:
        self.provider = provider
        self.repository = repository

    def run(self) -> list[Company]:
        companies = self.provider.discover()
        self.repository.save_many(companies)
        return companies
