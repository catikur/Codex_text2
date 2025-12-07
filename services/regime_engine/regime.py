"""Regime computation helpers."""
from __future__ import annotations

import math
from typing import Iterable, List, Sequence

import numpy as np


def realized_volatility(closes: Sequence[float]) -> float:
    if len(closes) < 2:
        return 0.0
    returns = np.diff(np.log(closes))
    return float(np.std(returns, ddof=1) * math.sqrt(252))


def classify_vol_regime(vol: float, thresholds: dict[str, float]) -> str:
    calm = thresholds.get("calm", 0.1)
    normal = thresholds.get("normal", 0.2)
    high = thresholds.get("high", 0.35)
    if vol < calm:
        return "calm"
    if vol < normal:
        return "normal"
    if vol < high:
        return "high"
    return "crisis"


def classify_risk_state(vol_regime: str, corr_value: float | None, corr_threshold: float = 0.35) -> str:
    if vol_regime in {"high", "crisis"} and (corr_value is not None and corr_value > corr_threshold):
        return "risk_off"
    if vol_regime == "normal":
        return "neutral"
    return "risk_on"
