"""Time utilities."""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Literal


Timeframe = Literal["1m", "5m", "1h", "1d"]


def now_utc() -> datetime:
    return datetime.now(timezone.utc)


def floor_timestamp(ts: datetime, timeframe: Timeframe) -> datetime:
    """Truncate timestamp to timeframe boundary."""

    if timeframe == "1m":
        return ts.replace(second=0, microsecond=0)
    if timeframe == "5m":
        minute = ts.minute - (ts.minute % 5)
        return ts.replace(minute=minute, second=0, microsecond=0)
    if timeframe == "1h":
        return ts.replace(minute=0, second=0, microsecond=0)
    if timeframe == "1d":
        return ts.replace(hour=0, minute=0, second=0, microsecond=0)
    return ts
