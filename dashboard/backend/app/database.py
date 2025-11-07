#!/usr/bin/env python3
"""
database.py
-----------
SQLAlchemy engine/session setup with .env support.
- Works with Neon (adds sslmode if missing)
- Uses psycopg3 by default (postgresql+psycopg)
- Falls back to SQLite for local dev when DATABASE_URL is absent
"""

from __future__ import annotations

import os
import warnings
from pathlib import Path
from urllib.parse import parse_qsl, urlencode, urlparse, urlunparse

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

# ----------------------------- ENV LOADING -----------------------------
BASE_DIR = Path(__file__).resolve().parent.parent  # .../backend
load_dotenv(BASE_DIR / ".env")

raw_url = os.getenv("DATABASE_URL", "").strip().strip("'").strip('"')


def _normalize_db_url(url: str) -> tuple[str, dict]:
    """
    Normalize DATABASE_URL for SQLAlchemy:
    - If empty -> SQLite fallback
    - If 'postgresql://' -> upgrade to 'postgresql+psycopg://'
    - Ensure sslmode=require for Neon if missing
    Returns: (normalized_url, connect_args)
    """
    if not url:
        warnings.warn(
            "DATABASE_URL not found; falling back to local SQLite (dev.db).",
            UserWarning,
        )
        sqlite_path = BASE_DIR / "dev.db"
        return f"sqlite:///{sqlite_path}", {"check_same_thread": False}

    # Force psycopg3 driver if user provided plain postgresql://
    if url.startswith("postgresql://") and "+psycopg" not in url:
        url = url.replace("postgresql://", "postgresql+psycopg://", 1)

    # If Neon host and sslmode missing, append it safely
    parsed = urlparse(url)
    host = parsed.hostname or ""
    query = dict(parse_qsl(parsed.query))

    if "neon.tech" in host and "sslmode" not in query:
        query["sslmode"] = "require"
        parsed = parsed._replace(query=urlencode(query))
        url = urlunparse(parsed)

    return url, {}  # no special connect_args for Postgres


DATABASE_URL, CONNECT_ARGS = _normalize_db_url(raw_url)

# ----------------------------- ENGINE / SESSION -----------------------------
engine = create_engine(
    DATABASE_URL,
    echo=True,  # set False in production
    future=True,
    pool_pre_ping=True,
    connect_args=CONNECT_ARGS,
)

SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False, future=True)

Base = declarative_base()


# ----------------------------- FASTAPI HELPERS -----------------------------
def get_db():
    """FastAPI dependency to provide a DB session."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    """
    Create all tables from models.
    Use only for local dev or tests; production should use Alembic migrations.
    """
    import app.models  # noqa: F401 - ensure models are imported

    Base.metadata.create_all(bind=engine)


# ----------------------------- SELF-TEST -----------------------------
if __name__ == "__main__":
    print("Testing DB connection to:", DATABASE_URL)
    try:
        with engine.connect() as conn:
            # simple no-op to confirm connection
            conn.exec_driver_sql("SELECT 1")
        print("✅ Connected successfully!")
    except Exception as e:
        print("❌ Connection failed:", e)
