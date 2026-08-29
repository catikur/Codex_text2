"""Config for risk daemon."""
from __future__ import annotations

from typing import Dict

from pydantic import Field
from pydantic_settings import SettingsConfigDict

from common.config_base import BaseAppSettings


class RiskSettings(BaseAppSettings):
    model_config = SettingsConfigDict(env_prefix="RISK_", env_file=".env", extra="ignore")

    db_dsn: str = Field(default="sqlite+pysqlite:///:memory:")
    policy_path: str = Field(default="config/risk_policy.yaml")
    primary_symbol: str = Field(default="BTCUSDT")
    interval_seconds: int = 15
