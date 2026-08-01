from dataclasses import dataclass, field
from typing import List, Optional


@dataclass(slots=True)
class Company:
    name: str
    website: Optional[str] = None
    industry: Optional[str] = None
    country: Optional[str] = None
    remote_ok: bool = False
    source: Optional[str] = None
    tags: List[str] = field(default_factory=list)


@dataclass(slots=True)
class Profile:
    name: str
    email: str
    phone: Optional[str] = None
    location: str = "Remote"
    headline: str = "Applied engineer"
    summary: str = "Applied engineer with strong software and research experience."
    skills: List[str] = field(default_factory=list)
    experience: List[dict] = field(default_factory=list)
    projects: List[dict] = field(default_factory=list)
    education: List[dict] = field(default_factory=list)
    certifications: List[dict] = field(default_factory=list)
    raw_context: List[str] = field(default_factory=list)
