from __future__ import annotations

from pathlib import Path

from sqlalchemy import create_engine
from sqlalchemy.exc import OperationalError
from sqlalchemy.orm import sessionmaker

from app.core.settings import settings
from app.infrastructure.database.models import Base

engine = None
SessionLocal = None


def init_db() -> None:
    global engine, SessionLocal
    if engine is None:
        try:
            engine = create_engine(settings.database_url, pool_pre_ping=True)
            if settings.database_url.startswith("sqlite"):
                sqlite_path = settings.database_url.removeprefix("sqlite:///")
                if sqlite_path:
                    Path(sqlite_path).parent.mkdir(parents=True, exist_ok=True)
            Base.metadata.create_all(bind=engine)
        except OperationalError:
            fallback_url = f"sqlite:///{Path(settings.artifact_root).parent.parent / 'storage' / 'jobsearch.db'}"
            engine = create_engine(fallback_url, connect_args={"check_same_thread": False})
            Base.metadata.create_all(bind=engine)
    if SessionLocal is None:
        SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
    Base.metadata.create_all(bind=engine)


def get_session():
    init_db()
    return SessionLocal()
