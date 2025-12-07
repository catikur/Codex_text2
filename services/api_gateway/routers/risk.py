"""Risk endpoints."""
from __future__ import annotations

from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from services.ingest_market.models import RegimeState, RiskRecommendation
from services.api_gateway.main import get_session

router = APIRouter(prefix="/risk", tags=["risk"])


@router.get("/current")
def current(session: Session = Depends(get_session)) -> dict:
    stmt = select(RiskRecommendation, RegimeState.risk_state).join(RegimeState, RegimeState.id == RiskRecommendation.regime_ref_id)
    stmt = stmt.order_by(RiskRecommendation.ts.desc()).limit(1)
    row = session.execute(stmt).first()
    if not row:
        raise HTTPException(status_code=404, detail="No recommendation")
    rec, risk_state = row
    return {
        "ts": rec.ts,
        "risk_state": risk_state,
        "gross_leverage_target": float(rec.gross_leverage_target),
        "net_beta_cap": float(rec.net_beta_cap),
        "altcoin_exposure_cap": float(rec.altcoin_exposure_cap),
        "enable_counterbook": rec.enable_counterbook,
        "notes": rec.notes,
    }


@router.get("/history")
def history(limit: int = 20, session: Session = Depends(get_session)) -> List[dict]:
    stmt = (
        select(RiskRecommendation, RegimeState.risk_state)
        .join(RegimeState, RegimeState.id == RiskRecommendation.regime_ref_id)
        .order_by(RiskRecommendation.ts.desc())
        .limit(limit)
    )
    rows = session.execute(stmt).all()
    result: List[dict] = []
    for rec, risk_state in rows:
        result.append(
            {
                "ts": rec.ts,
                "risk_state": risk_state,
                "gross_leverage_target": float(rec.gross_leverage_target),
                "net_beta_cap": float(rec.net_beta_cap),
                "altcoin_exposure_cap": float(rec.altcoin_exposure_cap),
                "enable_counterbook": rec.enable_counterbook,
                "notes": rec.notes,
            }
        )
    return result
