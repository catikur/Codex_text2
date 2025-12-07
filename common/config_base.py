"""Base configuration helpers using Pydantic settings."""
from __future__ import annotations

from functools import lru_cache
from typing import Optional

from pydantic_settings import BaseSettings, SettingsConfigDict


class BaseAppSettings(BaseSettings):
    """Base class for service configuration.

    Provides environment variable overrides and optional .env loading.
    """

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    env: str = "dev"
    log_level: str = "INFO"
    service_name: Optional[str] = None


@lru_cache()
def get_settings(cls: type[BaseAppSettings]) -> BaseAppSettings:
    """Load settings with caching to avoid repeated parsing."""

    return cls()  # type: ignore[arg-type]
