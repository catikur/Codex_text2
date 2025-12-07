"""Correlation helpers."""
from __future__ import annotations

from typing import Sequence

import numpy as np


def rolling_correlation(series_a: Sequence[float], series_b: Sequence[float]) -> float:
    if len(series_a) < 2 or len(series_a) != len(series_b):
        return 0.0
    return float(np.corrcoef(series_a, series_b)[0, 1])
