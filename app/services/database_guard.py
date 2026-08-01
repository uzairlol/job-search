from __future__ import annotations

from sqlalchemy import text
from sqlalchemy.exc import OperationalError

from app.infrastructure.database.session import get_session


class DatabaseGuard:
    def __init__(self) -> None:
        self.enabled = True

    def safe_session(self):
        try:
            session = get_session()
            session.execute(text("SELECT 1"))
            return session
        except OperationalError:
            self.enabled = False
            return None
