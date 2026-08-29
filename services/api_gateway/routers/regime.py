"""Regime endpoints."""
from __future__ import annotations

from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from services.ingest_market.models import RegimeState
from services.api_gateway.main import get_session

router = APIRouter(prefix="/regime", tags=["regime"])


@router.get("/current")
def current(symbol: str, session: Session = Depends(get_session)) -> dict:
    stmt = select(RegimeState).where(RegimeState.symbol == symbol).order_by(RegimeState.ts.desc()).limit(1)
    row = session.execute(stmt).scalar_one_or_none()
    if not row:
        raise HTTPException(status_code=404, detail="No regime state")
    return {
        "ts": row.ts,
        "symbol": row.symbol,
        "vol_regime": row.vol_regime,
        "vol_value": float(row.vol_value),
        "corr_symbol": row.corr_symbol,
        "corr_value": float(row.corr_value) if row.corr_value is not None else None,
        "risk_state": row.risk_state,
    }


@router.get("/history")
def history(symbol: str, limit: int = 20, session: Session = Depends(get_session)) -> List[dict]:
    stmt = (
        select(RegimeState)
        .where(RegimeState.symbol == symbol)
        .order_by(RegimeState.ts.desc())
        .limit(limit)
    )
    rows = session.execute(stmt).scalars().all()
    result: List[dict] = []
    for row in rows:
        result.append(
            {
                "ts": row.ts,
                "symbol": row.symbol,
                "vol_regime": row.vol_regime,
                "vol_value": float(row.vol_value),
                "corr_symbol": row.corr_symbol,
                "corr_value": float(row.corr_value) if row.corr_value is not None else None,
                "risk_state": row.risk_state,
            }
        )
    return result
