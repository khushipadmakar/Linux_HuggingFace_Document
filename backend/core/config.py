from dataclasses import dataclass
from pathlib import Path
import os

from dotenv import load_dotenv


load_dotenv()


def _env(name: str, default: str) -> str:
    return os.getenv(name, default)


def _env_int(name: str, default: int) -> int:
    try:
        return int(os.getenv(name, str(default)))
    except ValueError:
        return default


def _env_bool(name: str, default: bool) -> bool:
    raw = os.getenv(name)
    if raw is None:
        return default
    return raw.strip().lower() in {"1", "true", "yes", "y", "on"}


@dataclass(frozen=True)
class Settings:
    app_name: str = _env("AIDOC_APP_NAME", "AI Document Platform")
    app_version: str = _env("AIDOC_APP_VERSION", "1.0.0")
    api_prefix: str = _env("AIDOC_API_PREFIX", "/api")

    database_url: str = _env(
        "AIDOC_DATABASE_URL",
        "sqlite:///./storage/document_intelligence.db",
    )
    use_pgvector: bool = _env_bool("AIDOC_USE_PGVECTOR", False)

    upload_root: Path = Path(_env("AIDOC_UPLOAD_ROOT", "storage/uploads"))
    log_root: Path = Path(_env("AIDOC_LOG_ROOT", "storage/logs"))
    backup_root: Path = Path(_env("AIDOC_BACKUP_ROOT", "storage/backups"))

    hf_embedding_model: str = _env("AIDOC_HF_EMBEDDING_MODEL", "sentence-transformers/all-MiniLM-L6-v2")
    hf_summary_model: str = _env("AIDOC_HF_SUMMARY_MODEL", "sshleifer/distilbart-cnn-12-6")
    hf_qa_model: str = _env("AIDOC_HF_QA_MODEL", "deepset/roberta-base-squad2")
    llm_timeout_seconds: int = _env_int("AIDOC_LLM_TIMEOUT_SECONDS", 90)

    embedding_dimensions: int = _env_int("AIDOC_EMBEDDING_DIMENSIONS", 384)
    chunk_size: int = _env_int("AIDOC_CHUNK_SIZE", 900)
    chunk_overlap: int = _env_int("AIDOC_CHUNK_OVERLAP", 150)


settings = Settings()
