from __future__ import annotations

import json
from pathlib import Path
from typing import Any


class OutboxWriter:
    def __init__(self, output_dir: str | Path | None = None) -> None:
        self.output_dir = Path(output_dir or "artifacts/outbox")

    def write(self, company: str, subject: str, body: str) -> Path:
        self.output_dir.mkdir(parents=True, exist_ok=True)
        path = self.output_dir / f"{company.lower().replace(' ', '_')}.json"
        payload = {"company": company, "subject": subject, "body": body}
        path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
        return path
