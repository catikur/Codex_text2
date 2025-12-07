# Regime Engine

Computes realized volatility, correlation, and classifies vol/risk regimes based on stored OHLCV data.

## Run
```bash
python -m services.regime_engine.main
```

Key settings (ENV prefix `REGIME_`):
- `DB_DSN` — database connection string.
- `TIMEFRAME` — timeframe used for calculations (default `1d`).
- `VOL_WINDOW` — lookback window for volatility.
- `CORR_WINDOW` — lookback window for correlation.
