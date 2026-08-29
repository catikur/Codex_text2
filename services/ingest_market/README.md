# Ingest Market Service

Generates or fetches OHLCV bars for configured symbols/timeframes and writes them to the database.

## Run
```bash
python -m services.ingest_market.main
```

Environment variables (prefixed with `INGEST_`):
- `DB_DSN` — SQLAlchemy DSN.
- `DATA_SOURCE` — `mock` (default) or `ccxt`.
- `SYMBOLS` — comma-separated symbols.
- `TIMEFRAMES` — comma-separated timeframes.
