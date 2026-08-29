"""Entrypoint for market ingestion."""
from __future__ import annotations

import random
import time

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from common.logging import configure_logging, get_logger
from common.timeutils import floor_timestamp, now_utc
from services.ingest_market.config import IngestSettings
from services.ingest_market.models import Base
from services.ingest_market.repository import MarketRepository
from services.ingest_market.schemas import OHLCV

logger = get_logger(__name__)


def _mock_price(prev_price: float) -> float:
    return max(1.0, prev_price + random.gauss(0, prev_price * 0.001))


def generate_mock_ohlcv(symbol: str, timeframe: str, last_price: float) -> OHLCV:
    ts = floor_timestamp(now_utc(), timeframe)
    open_price = _mock_price(last_price)
    high = open_price * (1 + random.random() * 0.001)
    low = open_price * (1 - random.random() * 0.001)
    close = _mock_price(open_price)
    volume = random.random() * 10
    return OHLCV(
        symbol=symbol,
        timeframe=timeframe,
        ts=ts,
        open=open_price,
        high=high,
        low=low,
        close=close,
        volume=volume,
    )


def run_once(session: Session, settings: IngestSettings, last_prices: dict[str, float]) -> int:
    repo = MarketRepository(session)
    batch: list[OHLCV] = []
    for symbol in settings.symbols:
        for timeframe in settings.timeframes:
            last_price = last_prices.get(symbol, 100.0)
            row = generate_mock_ohlcv(symbol, timeframe, last_price)
            last_prices[symbol] = float(row.close)
            batch.append(row)
    inserted = repo.upsert_rows(batch)
    logger.info("ingested rows", extra={"count": inserted})
    return inserted


def main() -> None:
    settings = IngestSettings()
    configure_logging(settings.log_level, settings.service_name or "ingest_market")
    engine = create_engine(settings.db_dsn, future=True)
    SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False, future=True)
    Base.metadata.create_all(engine)

    last_prices: dict[str, float] = {symbol: 100.0 for symbol in settings.symbols}
    logger.info("starting ingestion loop")
    while True:
        with SessionLocal() as session:
            try:
                run_once(session, settings, last_prices)
                session.commit()
            except Exception as exc:  # pragma: no cover - runtime guard
                logger.exception("ingestion failed: %s", exc)
                session.rollback()
        time.sleep(settings.interval_seconds)


if __name__ == "__main__":
    main()
