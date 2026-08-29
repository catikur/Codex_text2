from datetime import datetime, timezone

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from services.ingest_market.models import Base
from services.ingest_market.repository import MarketRepository
from services.ingest_market.schemas import OHLCV


def create_session():
    engine = create_engine("sqlite+pysqlite:///:memory:", future=True)
    Base.metadata.create_all(engine)
    SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False, future=True)
    return SessionLocal()


def test_upsert_and_latest():
    session = create_session()
    repo = MarketRepository(session)
    ts = datetime.now(timezone.utc)
    row = OHLCV(symbol="BTC", timeframe="1h", ts=ts, open=1, high=2, low=0.5, close=1.5, volume=10)
    count = repo.upsert_rows([row])
    session.commit()
    assert count == 1
    latest = repo.latest_rows("BTC", "1h", limit=1)
    assert latest[0].close == 1.5
