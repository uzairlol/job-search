from __future__ import annotations

import subprocess


class OllamaPolisher:
    def __init__(self, model: str = "deepseek-r1:8b") -> None:
        self.model = model

    def polish(self, text: str) -> str:
        if not text.strip():
            return text

        try:
            result = subprocess.run(
                ["ollama", "run", self.model, text],
                capture_output=True,
                text=True,
                timeout=10,
            )
        except (FileNotFoundError, subprocess.TimeoutExpired):
            return text

        if result.returncode != 0:
            return text

        polished = result.stdout.strip()
        return polished or text
