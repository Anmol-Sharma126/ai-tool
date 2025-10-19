from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Optional

from dotenv import load_dotenv


@dataclass(frozen=True)
class AppConfig:
    environment: str
    openai_api_key: str
    model: str
    chroma_persist_dir: Optional[str]
    log_level: str


def load_config() -> AppConfig:
    load_dotenv()

    environment = os.getenv("APP_ENV", "development")
    openai_api_key = os.getenv("OPENAI_API_KEY", "")
    if not openai_api_key:
        raise RuntimeError("OPENAI_API_KEY is required")

    model = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
    chroma_persist_dir = os.getenv("CHROMA_PERSIST_DIR")
    log_level = os.getenv("LOG_LEVEL", "INFO")

    return AppConfig(
        environment=environment,
        openai_api_key=openai_api_key,
        model=model,
        chroma_persist_dir=chroma_persist_dir,
        log_level=log_level,
    )
