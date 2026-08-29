"""Repository for regime computations."""
from __future__ import annotations

from datetime import datetime
from typing import List, Sequence

from sqlalchemy import select
from sqlalchemy.orm import Session

from services.ingest_market.models import MarketOHLCV, RegimeState


class RegimeRepository:
    def __init__(self, session: Session):
        self.session = session

    def fetch_closes(self, symbol: str, timeframe: str, window: int) -> List[float]:
        stmt = (
            select(MarketOHLCV.close)
            .where(MarketOHLCV.symbol == symbol, MarketOHLCV.timeframe == timeframe)
            .order_by(MarketOHLCV.ts.desc())
            .limit(window)
        )
        rows = list(self.session.execute(stmt).scalars())
        return list(reversed([float(v) for v in rows]))

    def save_regime(
        self,
        ts: datetime,
        symbol: str,
        vol_regime: str,
        vol_value: float,
        corr_symbol: str | None,
        corr_value: float | None,
        risk_state: str,
    ) -> RegimeState:
        regime = RegimeState(
            ts=ts,
            symbol=symbol,
            vol_regime=vol_regime,
            vol_value=vol_value,
            corr_symbol=corr_symbol,
            corr_value=corr_value,
            risk_state=risk_state,
        )
        self.session.add(regime)
        self.session.flush()
        return regime

    def latest_regime(self, symbol: str) -> RegimeState | None:
        stmt = (
            select(RegimeState).where(RegimeState.symbol == symbol).order_by(RegimeState.ts.desc()).limit(1)
        )
        return self.session.execute(stmt).scalar_one_or_none()
