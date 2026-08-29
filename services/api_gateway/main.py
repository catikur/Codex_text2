"""API Gateway service."""
from __future__ import annotations

from fastapi import Depends, FastAPI
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from common.logging import configure_logging, get_logger
from services.api_gateway.config import APIGatewaySettings
from services.api_gateway.routers import health, regime, risk
from services.ingest_market.models import Base

logger = get_logger(__name__)

settings = APIGatewaySettings()
configure_logging(settings.log_level, settings.service_name or "api_gateway")
engine = create_engine(settings.db_dsn, future=True)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False, future=True)
Base.metadata.create_all(engine)


def get_session() -> Session:
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()


app = FastAPI(title="api-gateway")
app.include_router(health.router)
app.include_router(regime.router)
app.include_router(risk.router)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("services.api_gateway.main:app", host="0.0.0.0", port=8000, reload=False)
