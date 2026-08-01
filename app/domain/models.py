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
