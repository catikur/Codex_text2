"""SQLAlchemy models for market data and regimes."""
from __future__ import annotations

from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, Numeric, String, UniqueConstraint
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


class MarketOHLCV(Base):
    __tablename__ = "market_ohlcv"
    __table_args__ = (UniqueConstraint("symbol", "timeframe", "ts", name="uq_symbol_timeframe_ts"),)

    id = Column(Integer, primary_key=True)
    symbol = Column(String, nullable=False)
    timeframe = Column(String, nullable=False)
    ts = Column(DateTime(timezone=True), nullable=False)
    open = Column(Numeric, nullable=False)
    high = Column(Numeric, nullable=False)
    low = Column(Numeric, nullable=False)
    close = Column(Numeric, nullable=False)
    volume = Column(Numeric, nullable=False)


class RegimeState(Base):
    __tablename__ = "regime_state"

    id = Column(Integer, primary_key=True)
    ts = Column(DateTime(timezone=True), nullable=False)
    symbol = Column(String, nullable=False)
    vol_regime = Column(String, nullable=False)
    vol_value = Column(Numeric, nullable=False)
    corr_symbol = Column(String, nullable=True)
    corr_value = Column(Numeric, nullable=True)
    risk_state = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), nullable=False, default=datetime.utcnow)

    recommendations = relationship("RiskRecommendation", back_populates="regime", lazy="selectin")


class RiskRecommendation(Base):
    __tablename__ = "risk_recommendation"

    id = Column(Integer, primary_key=True)
    ts = Column(DateTime(timezone=True), nullable=False)
    regime_ref_id = Column(Integer, ForeignKey("regime_state.id"))
    gross_leverage_target = Column(Numeric, nullable=False)
    net_beta_cap = Column(Numeric, nullable=False)
    altcoin_exposure_cap = Column(Numeric, nullable=False)
    enable_counterbook = Column(Boolean, nullable=False, default=False)
    notes = Column(String, nullable=True)

    regime = relationship("RegimeState", back_populates="recommendations")
