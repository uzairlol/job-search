import os
from dataclasses import dataclass
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parents[2]
DEFAULT_SQLITE_DB = BASE_DIR / "storage" / "jobsearch.db"


@dataclass(frozen=True)
class Settings:
    database_url: str = os.getenv("DATABASE_URL", f"sqlite:///{DEFAULT_SQLITE_DB.as_posix()}")
    smtp_host: str = os.getenv("SMTP_HOST", "smtp.gmail.com")
    smtp_port: int = int(os.getenv("SMTP_PORT", "587"))
    smtp_user: str = os.getenv("SMTP_USER", "")
    smtp_password: str = os.getenv("SMTP_PASSWORD", "")
    ollama_model: str = os.getenv("OLLAMA_MODEL", "deepseek-r1:8b")
    profile_dir: str = os.getenv("PROFILE_DIR", str(BASE_DIR / "user_profile"))
    artifact_root: str = os.getenv("ARTIFACT_ROOT", str(BASE_DIR / "storage" / "artifacts"))
    prompt_dir: str = os.getenv("PROMPT_DIR", str(BASE_DIR / "app" / "prompts"))
    default_company_focus: str = os.getenv("DEFAULT_COMPANY_FOCUS", "remote ai ml research")


settings = Settings()
