"""Schemas for risk daemon."""
from __future__ import annotations

from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class RiskRecommendationSchema(BaseModel):
    ts: datetime
    risk_state: str
    gross_leverage_target: float
    net_beta_cap: float
    altcoin_exposure_cap: float
    enable_counterbook: bool
    notes: Optional[str] = None
