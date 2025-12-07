"""Database helpers for SQLAlchemy."""
from __future__ import annotations

import os
from contextlib import contextmanager
from typing import Generator

from sqlalchemy import create_engine, text
from sqlalchemy.engine import Engine
from sqlalchemy.orm import sessionmaker

DEFAULT_DSN = os.getenv("DB_DSN", "sqlite+pysqlite:///:memory:")

engine: Engine = create_engine(DEFAULT_DSN, echo=False, future=True)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False, future=True)


@contextmanager
def session_scope() -> Generator:
    """Provide a transactional scope around a series of operations."""

    session = SessionLocal()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()


def run_init_sql(sql_path: str) -> None:
    """Run initialization SQL (used for migrations in simple setups)."""

    with open(sql_path, "r", encoding="utf-8") as file:
        sql_statements = file.read()
    with engine.connect() as conn:
        for statement in filter(None, sql_statements.split(";")):
            stmt = statement.strip()
            if stmt:
                conn.execute(text(stmt))
        conn.commit()
