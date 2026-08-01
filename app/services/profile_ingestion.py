from __future__ import annotations

from pathlib import Path
from typing import Any

from app.core.settings import settings
from app.services.database_guard import DatabaseGuard


class ProfileIngestionService:
    def __init__(self, profile_dir: str | Path | None = None) -> None:
        self.profile_dir = Path(profile_dir or settings.profile_dir)
        self.profile_dir.mkdir(parents=True, exist_ok=True)
        self.database_guard = DatabaseGuard()

    def ingest(self) -> list[dict[str, Any]]:
        documents = []
        for path in sorted(self.profile_dir.glob("*")):
            if path.is_file() and path.suffix.lower() in {".md", ".txt", ".json"}:
                payload = path.read_text(encoding="utf-8")
                documents.append({"name": path.name, "size": path.stat().st_size})

                session = self.database_guard.safe_session()
                if session is not None:
                    from app.infrastructure.database.repositories import ProfileRepository

                    with session:
                        repository = ProfileRepository(session)
                        repository.store_document(path.name, payload)
                else:
                    print(f"[ingest] database unavailable; keeping {path.name} in the local profile directory only")
        return documents
