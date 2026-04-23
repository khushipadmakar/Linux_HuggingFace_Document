from collections.abc import Generator

from sqlalchemy import create_engine, inspect, text
from sqlalchemy.orm import Session, sessionmaker

from backend.core.config import settings
from backend.db.models import Base


connect_args = {}
if settings.database_url.startswith("sqlite"):
    connect_args = {"check_same_thread": False}

engine = create_engine(settings.database_url, pool_pre_ping=True, future=True, connect_args=connect_args)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False, future=True)


def _safe_exec(statement: str) -> None:
    try:
        with engine.begin() as conn:
            conn.execute(text(statement))
    except Exception:
        # Best-effort schema healing for legacy local databases.
        pass


def _migrate_legacy_schema() -> None:
    inspector = inspect(engine)
    tables = set(inspector.get_table_names())
    if "uploaded_documents" not in tables:
        return

    column_names = {col["name"] for col in inspector.get_columns("uploaded_documents")}

    if "filepath" not in column_names and "file_path" in column_names:
        _safe_exec("ALTER TABLE uploaded_documents RENAME COLUMN file_path TO filepath")
        column_names.discard("file_path")
        column_names.add("filepath")

    if "filepath" not in column_names:
        _safe_exec("ALTER TABLE uploaded_documents ADD COLUMN filepath VARCHAR(1024)")

    if "file_type" not in column_names:
        _safe_exec("ALTER TABLE uploaded_documents ADD COLUMN file_type VARCHAR(32) DEFAULT 'txt'")

    if "size_bytes" not in column_names:
        _safe_exec("ALTER TABLE uploaded_documents ADD COLUMN size_bytes INTEGER DEFAULT 0")

    if "processed_at" not in column_names:
        _safe_exec("ALTER TABLE uploaded_documents ADD COLUMN processed_at TIMESTAMP NULL")

    # Backfill for legacy rows.
    _safe_exec("UPDATE uploaded_documents SET filepath = COALESCE(filepath, '')")
    _safe_exec("UPDATE uploaded_documents SET file_type = COALESCE(file_type, 'txt')")
    _safe_exec("UPDATE uploaded_documents SET size_bytes = COALESCE(size_bytes, 0)")


def init_db() -> None:
    if settings.use_pgvector and settings.database_url.startswith("postgresql"):
        with engine.begin() as conn:
            conn.execute(text("CREATE EXTENSION IF NOT EXISTS vector"))
    _migrate_legacy_schema()
    Base.metadata.create_all(bind=engine)


def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
