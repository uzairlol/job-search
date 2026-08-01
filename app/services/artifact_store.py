from __future__ import annotations

import shutil
from pathlib import Path
from datetime import datetime

from app.core.settings import settings


class ArtifactStore:
    def __init__(self, root: str | Path | None = None) -> None:
        self.root = Path(root or settings.artifact_root)
        self.root.mkdir(parents=True, exist_ok=True)

    def make_run_dir(self, run_name: str | None = None) -> Path:
        timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
        run_name = run_name or f"cycle_{timestamp}"
        run_dir = self.root / run_name
        run_dir.mkdir(parents=True, exist_ok=True)
        return run_dir

    def clean(self) -> None:
        if self.root.exists():
            shutil.rmtree(self.root)
            self.root.mkdir(parents=True, exist_ok=True)
