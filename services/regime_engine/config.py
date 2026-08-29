"""Config for regime engine."""
from __future__ import annotations

from typing import Dict, List, Tuple

from pydantic import Field
from pydantic_settings import SettingsConfigDict

from common.config_base import BaseAppSettings


class RegimeSettings(BaseAppSettings):
    model_config = SettingsConfigDict(env_prefix="REGIME_", env_file=".env", extra="ignore")

    db_dsn: str = Field(default="sqlite+pysqlite:///:memory:")
    symbols: List[str] = Field(default_factory=lambda: ["BTCUSDT", "SPX"])
    timeframe: str = "1d"
    vol_window: int = 20
    vol_thresholds: Dict[str, float] = Field(
        default_factory=lambda: {
            "calm": 0.10,
            "normal": 0.20,
            "high": 0.35,
        }
    )
    corr_pairs: List[Tuple[str, str]] = Field(default_factory=lambda: [("BTCUSDT", "SPX")])
    corr_window: int = 20
    interval_seconds: int = 10
