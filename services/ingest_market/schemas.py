"""Pydantic schemas for ingestion."""
from __future__ import annotations

from datetime import datetime
from typing import List

from pydantic import BaseModel


class OHLCV(BaseModel):
    symbol: str
    timeframe: str
    ts: datetime
    open: float
    high: float
    low: float
    close: float
    volume: float


class IngestBatch(BaseModel):
    rows: List[OHLCV]
