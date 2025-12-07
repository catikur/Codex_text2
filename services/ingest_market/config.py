"""Configuration for market ingestion service."""
from __future__ import annotations

from typing import List

from pydantic import Field
from pydantic_settings import SettingsConfigDict

from common.config_base import BaseAppSettings


class IngestSettings(BaseAppSettings):
    model_config = SettingsConfigDict(env_prefix="INGEST_", env_file=".env", extra="ignore")

    db_dsn: str = Field(default="sqlite+pysqlite:///:memory:")
    data_source: str = Field(default="mock", description="mock or ccxt")
    symbols: List[str] = Field(default_factory=lambda: ["BTCUSDT", "SPX"])
    timeframes: List[str] = Field(default_factory=lambda: ["1h", "1d"])
    interval_seconds: int = 5
