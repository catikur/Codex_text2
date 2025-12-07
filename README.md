# Trading Brain (Phase 1)

An event-driven, regime-aware trading system skeleton. Phase 1 focuses on infrastructure, market data ingestion, regime detection, risk policy output, and an API gateway.

## Architecture

- **ingest_market**: produces OHLCV time series (mocked by default) and stores them in Postgres/TimescaleDB.
- **regime_engine**: computes realized volatility, correlations, classifies vol and risk regimes, and persists `regime_state`.
- **risk_daemon**: maps regime state to portfolio guardrails and publishes `risk_recommendation` alongside Prometheus metrics.
- **api_gateway**: unified FastAPI surface for health, regime snapshots, and risk recommendations.
- **common**: logging, configuration, DB helpers, and stubs for messaging.

Database tables:
- `market_ohlcv` — OHLCV history per symbol and timeframe.
- `regime_state` — volatility regime, correlation snapshot, and derived risk state.
- `risk_recommendation` — policy outputs keyed to a regime_state row.

## Running locally

Dependencies: Docker + docker-compose.

```bash
make up      # start postgres and services
make down    # stop stack
make tests   # run unit tests with pytest
```

Services expose FastAPI endpoints (defaults):
- API Gateway: `http://localhost:8000`
- Risk Daemon: `http://localhost:8002`

Example queries:
```bash
curl http://localhost:8000/health/live
curl "http://localhost:8000/regime/current?symbol=BTCUSDT"
curl http://localhost:8002/risk/current
```

## Development notes

- Python 3.11, FastAPI, SQLAlchemy, Pydantic, pytest.
- Default data source is a deterministic mock generator; switch via `INGEST_DATA_SOURCE` when adding real feeds.
- Configurable risk policy in `config/risk_policy.yaml`.

## Project layout

```
common/                 # shared helpers
services/
  ingest_market/
  regime_engine/
  risk_daemon/
  api_gateway/
infra/                  # init SQL, monitoring placeholders
config/                 # risk policy
```
