"""Repository layer for market ingestion."""
from __future__ import annotations

from typing import Iterable, List

from sqlalchemy import select
from sqlalchemy.orm import Session

from services.ingest_market.models import MarketOHLCV
from services.ingest_market.schemas import OHLCV


class MarketRepository:
    """Persist and query OHLCV rows."""

    def __init__(self, session: Session):
        self.session = session

    def upsert_rows(self, rows: Iterable[OHLCV]) -> int:
        count = 0
        for row in rows:
            existing = self.session.execute(
                select(MarketOHLCV).where(
                    MarketOHLCV.symbol == row.symbol,
                    MarketOHLCV.timeframe == row.timeframe,
                    MarketOHLCV.ts == row.ts,
                )
            ).scalar_one_or_none()
            if existing:
                existing.open = row.open
                existing.high = row.high
                existing.low = row.low
                existing.close = row.close
                existing.volume = row.volume
            else:
                self.session.add(
                    MarketOHLCV(
                        symbol=row.symbol,
                        timeframe=row.timeframe,
                        ts=row.ts,
                        open=row.open,
                        high=row.high,
                        low=row.low,
                        close=row.close,
                        volume=row.volume,
                    )
                )
            count += 1
        return count

    def latest_rows(self, symbol: str, timeframe: str, limit: int = 100) -> List[MarketOHLCV]:
        stmt = (
            select(MarketOHLCV)
            .where(MarketOHLCV.symbol == symbol, MarketOHLCV.timeframe == timeframe)
            .order_by(MarketOHLCV.ts.desc())
            .limit(limit)
        )
        return list(self.session.execute(stmt).scalars())
