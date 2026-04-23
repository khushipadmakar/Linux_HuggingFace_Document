from __future__ import annotations

import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path

from backend.core.config import settings


logger = logging.getLogger("ai_doc_platform")


def configure_logger() -> None:
    settings.log_root.mkdir(parents=True, exist_ok=True)
    log_file = Path(settings.log_root) / "app.log"

    if logger.handlers:
        return

    logger.setLevel(logging.INFO)
    handler = RotatingFileHandler(log_file, maxBytes=5_000_000, backupCount=5)
    formatter = logging.Formatter("%(asctime)s [%(levelname)s] %(message)s")
    handler.setFormatter(formatter)
    logger.addHandler(handler)


def log_info(message: str) -> None:
    configure_logger()
    logger.info(message)
