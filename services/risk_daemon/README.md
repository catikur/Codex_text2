# Risk Daemon

Transforms regime states into risk recommendations based on configurable policy files and exposes them via FastAPI and Prometheus metrics.

## Run
```bash
python -m services.risk_daemon.main
```

Environment variables (prefix `RISK_`):
- `DB_DSN` — database connection string.
- `POLICY_PATH` — path to YAML policy (default `config/risk_policy.yaml`).
- `PRIMARY_SYMBOL` — symbol whose regime drives policy (default `BTCUSDT`).
