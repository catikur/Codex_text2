from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from services.ingest_market.config import IngestSettings
from services.ingest_market.main import run_once
from services.ingest_market.models import Base


def test_run_once_generates_rows():
    settings = IngestSettings()
    settings.symbols = ["BTCUSDT"]
    settings.timeframes = ["1h"]
    engine = create_engine("sqlite+pysqlite:///:memory:", future=True)
    Base.metadata.create_all(engine)
    SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False, future=True)
    last_prices = {}
    with SessionLocal() as session:
        inserted = run_once(session, settings, last_prices)
        session.commit()
    assert inserted == 1
