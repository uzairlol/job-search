from typing import Protocol

from app.domain.models import Company


class CompanyDiscoveryProvider(Protocol):
    def discover(self) -> list[Company]:
        ...


class CompanyRepository(Protocol):
    def save_many(self, companies: list[Company]) -> None:
        ...

    def list_all(self) -> list[Company]:
        ...
