"""Application settings.

All configuration comes from environment variables. In local development,
python-dotenv loads them from a `.env` file at the project root, so secrets
never appear in source code.

Usage:
    from keystone.config import get_settings
    settings = get_settings()
"""

from __future__ import annotations

import os
from functools import lru_cache
from pathlib import Path
from typing import Literal

from dotenv import load_dotenv
from pydantic import BaseModel, Field, SecretStr

# Project root = the folder that contains the `keystone` package.
PROJECT_ROOT = Path(__file__).resolve().parent.parent


class Settings(BaseModel):
    """Typed, validated configuration for the whole app."""

    # SecretStr hides the value in logs and repr(); call .get_secret_value() to use it.
    # Optional for now: Phase 1 makes no OpenAI calls, so the app must start without a key.
    openai_api_key: SecretStr | None = None
    openai_chat_model: str = "gpt-4o-mini"
    openai_embedding_model: str = "text-embedding-3-small"

    chroma_dir: Path = PROJECT_ROOT / "data" / "chroma"
    chroma_collection: str = "keystone"

    app_env: Literal["dev", "test", "prod"] = "dev"

    # Where the source documents live (used from Phase 2).
    raw_data_dir: Path = Field(default=PROJECT_ROOT / "data" / "raw")

    @property
    def openai_configured(self) -> bool:
        """True if a real-looking key is set (not empty, not the .env.example placeholder)."""
        if self.openai_api_key is None:
            return False
        key = self.openai_api_key.get_secret_value().strip()
        return bool(key) and key != "sk-replace-me"


def _resolve_path(value: str | None, default: Path) -> Path:
    """Relative paths in .env are resolved against the project root, not the CWD."""
    if not value:
        return default
    path = Path(value)
    return path if path.is_absolute() else PROJECT_ROOT / path


@lru_cache
def get_settings() -> Settings:
    """Load .env (if present) and build Settings once; later calls reuse the cached object.

    Real environment variables win over values in .env (override=False),
    which is what you want in CI or production.
    """
    load_dotenv(PROJECT_ROOT / ".env", override=False)

    defaults = Settings()
    return Settings(
        openai_api_key=os.getenv("OPENAI_API_KEY") or None,
        openai_chat_model=os.getenv("OPENAI_CHAT_MODEL", defaults.openai_chat_model),
        openai_embedding_model=os.getenv(
            "OPENAI_EMBEDDING_MODEL", defaults.openai_embedding_model
        ),
        chroma_dir=_resolve_path(os.getenv("CHROMA_DIR"), defaults.chroma_dir),
        chroma_collection=os.getenv("CHROMA_COLLECTION", defaults.chroma_collection),
        app_env=os.getenv("APP_ENV", defaults.app_env),
    )
