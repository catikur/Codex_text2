"""Entrypoint for regime engine."""
from __future__ import annotations

import time
from datetime import datetime

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from common.logging import configure_logging, get_logger
from common.timeutils import now_utc
from services.ingest_market.models import Base
from services.regime_engine.config import RegimeSettings
from services.regime_engine.correlation import rolling_correlation
from services.regime_engine.regime import classify_risk_state, classify_vol_regime, realized_volatility
from services.regime_engine.repository import RegimeRepository

logger = get_logger(__name__)


def compute_and_store(session, settings: RegimeSettings) -> None:
    repo = RegimeRepository(session)
    for symbol in settings.symbols:
        closes = repo.fetch_closes(symbol, settings.timeframe, settings.vol_window)
        vol = realized_volatility(closes)
        vol_regime = classify_vol_regime(vol, settings.vol_thresholds)
        corr_value = None
        corr_symbol = None
        for pair in settings.corr_pairs:
            if symbol == pair[0]:
                other_symbol = pair[1]
                other_closes = repo.fetch_closes(other_symbol, settings.timeframe, settings.corr_window)
                min_len = min(len(closes), len(other_closes))
                if min_len > 1:
                    corr_value = rolling_correlation(closes[-min_len:], other_closes[-min_len:])
                    corr_symbol = other_symbol
                break
        risk_state = classify_risk_state(vol_regime, corr_value)
        repo.save_regime(now_utc(), symbol, vol_regime, vol, corr_symbol, corr_value, risk_state)
    session.commit()


def main() -> None:
    settings = RegimeSettings()
    configure_logging(settings.log_level, settings.service_name or "regime_engine")
    engine = create_engine(settings.db_dsn, future=True)
    SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False, future=True)
    Base.metadata.create_all(engine)
    logger.info("starting regime engine loop")
    while True:
        with SessionLocal() as session:
            try:
                compute_and_store(session, settings)
            except Exception as exc:  # pragma: no cover - runtime guard
                logger.exception("regime computation failed: %s", exc)
                session.rollback()
        time.sleep(settings.interval_seconds)


if __name__ == "__main__":
    main()
