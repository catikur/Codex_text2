import math

from services.regime_engine.regime import classify_risk_state, classify_vol_regime, realized_volatility


def test_realized_volatility_small_series():
    closes = [100, 101, 102, 103]
    vol = realized_volatility(closes)
    assert vol > 0


def test_classify_vol_regime_thresholds():
    thresholds = {"calm": 0.1, "normal": 0.2, "high": 0.3}
    assert classify_vol_regime(0.05, thresholds) == "calm"
    assert classify_vol_regime(0.15, thresholds) == "normal"
    assert classify_vol_regime(0.25, thresholds) == "high"
    assert classify_vol_regime(0.35, thresholds) == "crisis"


def test_classify_risk_state():
    assert classify_risk_state("crisis", 0.4) == "risk_off"
    assert classify_risk_state("normal", 0.1) == "neutral"
    assert classify_risk_state("calm", None) == "risk_on"
