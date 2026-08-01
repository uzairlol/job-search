from __future__ import annotations

from dataclasses import dataclass
from typing import List


@dataclass(slots=True)
class DiscoveryOpportunity:
    name: str
    website: str | None
    industry: str | None
    country: str | None
    remote_ok: bool
    score: float
    source: str
    tags: List[str]


class CompanyDiscoveryService:
    """Rule-based discovery service that prioritizes globally remote-friendly opportunities."""

    def discover(self, target_role: str = "Machine Learning Engineer") -> list[DiscoveryOpportunity]:
        seed = [
            DiscoveryOpportunity(
                name="Northstar Labs",
                website="https://northstar.example",
                industry="AI",
                country="Remote",
                remote_ok=True,
                score=96.0,
                source="seed",
                tags=["ai", "remote", "ml"],
            ),
            DiscoveryOpportunity(
                name="Open Research Collective",
                website="https://openresearch.example",
                industry="Research",
                country="Remote",
                remote_ok=True,
                score=92.0,
                source="seed",
                tags=["research", "remote", "ml"],
            ),
            DiscoveryOpportunity(
                name="Helio Robotics",
                website="https://heliorobotics.example",
                industry="Robotics",
                country="Remote",
                remote_ok=True,
                score=88.0,
                source="seed",
                tags=["robotics", "remote", "engineering"],
            ),
            DiscoveryOpportunity(
                name="Atlas Data Works",
                website="https://atlasdata.example",
                industry="Data",
                country="US",
                remote_ok=False,
                score=74.0,
                source="seed",
                tags=["data", "analytics"],
            ),
        ]

        target_keywords = self._role_keywords(target_role)
        ranked = []
        for opportunity in seed:
            keyword_score = sum(1 for keyword in target_keywords if keyword in " ".join(opportunity.tags + [opportunity.industry or ""]))
            remote_bonus = 8 if opportunity.remote_ok else 0
            score = opportunity.score + keyword_score * 3 + remote_bonus
            ranked.append(
                DiscoveryOpportunity(
                    name=opportunity.name,
                    website=opportunity.website,
                    industry=opportunity.industry,
                    country=opportunity.country,
                    remote_ok=opportunity.remote_ok,
                    score=score,
                    source=opportunity.source,
                    tags=opportunity.tags,
                )
            )

        ranked.sort(key=lambda item: item.score, reverse=True)
        return ranked

    def _role_keywords(self, target_role: str) -> list[str]:
        role = target_role.lower()
        keywords = []
        if "machine learning" in role or "ml" in role:
            keywords.extend(["ml", "ai", "research"])
        if "engineer" in role:
            keywords.append("engineering")
        if "data" in role:
            keywords.append("data")
        return keywords
