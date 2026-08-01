from app.domain.models import Company


class CompanyDiscoveryService:
    """A thin service that produces candidate companies for the first phase."""

    def discover(self) -> list[Company]:
        return [
            Company(
                name="Example AI Labs",
                website="https://example.ai",
                industry="AI",
                country="Remote",
                remote_ok=True,
                source="seed",
                tags=["ai", "remote"],
            ),
            Company(
                name="Open Research Co",
                website="https://openresearch.co",
                industry="Research",
                country="US",
                remote_ok=True,
                source="seed",
                tags=["research", "ml"],
            ),
        ]
