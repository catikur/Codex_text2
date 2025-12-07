"""API gateway configuration."""
from __future__ import annotations

from pydantic import Field
from pydantic_settings import SettingsConfigDict

from common.config_base import BaseAppSettings


class APIGatewaySettings(BaseAppSettings):
    model_config = SettingsConfigDict(env_prefix="API_", env_file=".env", extra="ignore")

    db_dsn: str = Field(default="sqlite+pysqlite:///:memory:")
