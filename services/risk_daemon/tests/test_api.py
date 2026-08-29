from datetime import datetime, timezone

from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from services.ingest_market.models import Base, RegimeState
from services.risk_daemon import main


def test_get_current_recommendation():
    # prepare DB
    engine = create_engine("sqlite+pysqlite:///:memory:", future=True)
    Base.metadata.create_all(engine)
    SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False, future=True)
    main.context.engine = engine
    main.context.SessionLocal = SessionLocal

    with SessionLocal() as session:
        regime = RegimeState(
            ts=datetime.now(timezone.utc),
            symbol=main.settings.primary_symbol,
            vol_regime="calm",
            vol_value=0.05,
            corr_symbol=None,
            corr_value=None,
            risk_state="risk_on",
        )
        session.add(regime)
        session.commit()
        main.context.policy = main.RiskPolicy(main.settings.policy_path)
        main.evaluate_policy(session)

    client = TestClient(main.app)
    response = client.get("/risk/current")
    assert response.status_code == 200
    data = response.json()
    assert data["risk_state"] == "risk_on"
