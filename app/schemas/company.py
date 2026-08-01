from pydantic import BaseModel, Field


class CompanyRead(BaseModel):
    name: str = Field(..., min_length=1)
    website: str | None = None
    industry: str | None = None
    country: str | None = None
    remote_ok: bool = False
    source: str | None = None
    tags: list[str] = []
