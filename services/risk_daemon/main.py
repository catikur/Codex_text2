"""Risk daemon service."""
from __future__ import annotations

import threading
import time
from typing import List, Optional

from fastapi import FastAPI, HTTPException
from prometheus_client import Gauge, generate_latest
from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session, sessionmaker
from starlette.responses import Response

from common.logging import configure_logging, get_logger
from services.ingest_market.models import Base, RegimeState, RiskRecommendation
from services.risk_daemon.config import RiskSettings
from services.risk_daemon.policies import RiskPolicy
from services.risk_daemon.schemas import RiskRecommendationSchema

logger = get_logger(__name__)

app = FastAPI(title="risk-daemon")

current_risk_gauge = Gauge("current_risk_state", "Current risk state", labelnames=["state"])
leverage_gauge = Gauge("gross_leverage_target", "Gross leverage target")
beta_cap_gauge = Gauge("net_beta_cap", "Net beta cap")
alt_cap_gauge = Gauge("altcoin_exposure_cap", "Altcoin exposure cap")


class AppContext:
    def __init__(self, settings: RiskSettings):
        self.settings = settings
        self.engine = create_engine(settings.db_dsn, future=True)
        self.SessionLocal = sessionmaker(bind=self.engine, autoflush=False, autocommit=False, future=True)
        Base.metadata.create_all(self.engine)
        self.policy = RiskPolicy(settings.policy_path)

    def get_session(self) -> Session:
        return self.SessionLocal()


settings = RiskSettings()
configure_logging(settings.log_level, settings.service_name or "risk_daemon")
context = AppContext(settings)


def evaluate_policy(session: Session) -> Optional[RiskRecommendation]:
    stmt = select(RegimeState).where(RegimeState.symbol == settings.primary_symbol).order_by(RegimeState.ts.desc())
    regime = session.execute(stmt).scalar_one_or_none()
    if not regime:
        return None
    recommendation = context.policy.recommend(regime)
    session.add(recommendation)
    session.commit()
    update_metrics(regime.risk_state, recommendation)
    return recommendation


def update_metrics(risk_state: str, rec: RiskRecommendation) -> None:
    current_risk_gauge.labels(state=risk_state).set(1)
    leverage_gauge.set(float(rec.gross_leverage_target))
    beta_cap_gauge.set(float(rec.net_beta_cap))
    alt_cap_gauge.set(float(rec.altcoin_exposure_cap))


@app.on_event("startup")
def startup_event() -> None:
    def loop() -> None:  # pragma: no cover - runtime loop
        while True:
            with context.get_session() as session:
                try:
                    evaluate_policy(session)
                except Exception as exc:
                    logger.exception("policy evaluation failed: %s", exc)
                    session.rollback()
            time.sleep(settings.interval_seconds)

    threading.Thread(target=loop, daemon=True).start()


@app.get("/risk/current", response_model=RiskRecommendationSchema)
def get_current() -> RiskRecommendationSchema:
    with context.get_session() as session:
        stmt = select(RiskRecommendation, RegimeState.risk_state).join(RegimeState, RegimeState.id == RiskRecommendation.regime_ref_id)
        stmt = stmt.order_by(RiskRecommendation.ts.desc()).limit(1)
        row = session.execute(stmt).first()
        if not row:
            raise HTTPException(status_code=404, detail="No recommendation")
        rec, risk_state = row
        return RiskRecommendationSchema(
            ts=rec.ts,
            risk_state=risk_state,
            gross_leverage_target=float(rec.gross_leverage_target),
            net_beta_cap=float(rec.net_beta_cap),
            altcoin_exposure_cap=float(rec.altcoin_exposure_cap),
            enable_counterbook=rec.enable_counterbook,
            notes=rec.notes,
        )


@app.get("/risk/history", response_model=List[RiskRecommendationSchema])
def get_history(limit: int = 20) -> List[RiskRecommendationSchema]:
    with context.get_session() as session:
        stmt = (
            select(RiskRecommendation, RegimeState.risk_state)
            .join(RegimeState, RegimeState.id == RiskRecommendation.regime_ref_id)
            .order_by(RiskRecommendation.ts.desc())
            .limit(limit)
        )
        rows = session.execute(stmt).all()
        result: List[RiskRecommendationSchema] = []
        for rec, risk_state in rows:
            result.append(
                RiskRecommendationSchema(
                    ts=rec.ts,
                    risk_state=risk_state,
                    gross_leverage_target=float(rec.gross_leverage_target),
                    net_beta_cap=float(rec.net_beta_cap),
                    altcoin_exposure_cap=float(rec.altcoin_exposure_cap),
                    enable_counterbook=rec.enable_counterbook,
                    notes=rec.notes,
                )
            )
        return result


@app.get("/metrics")
def metrics() -> Response:
    return Response(generate_latest(), media_type="text/plain; version=0.0.4")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("services.risk_daemon.main:app", host="0.0.0.0", port=8002, reload=False)
