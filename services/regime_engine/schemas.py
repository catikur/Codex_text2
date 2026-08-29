"""Schemas for regime engine."""
from __future__ import annotations

from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class RegimeRecord(BaseModel):
    ts: datetime
    symbol: str
    vol_regime: str
    vol_value: float
    corr_symbol: Optional[str] = None
    corr_value: Optional[float] = None
    risk_state: str
