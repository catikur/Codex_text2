# API Gateway

FastAPI gateway exposing health checks plus the latest regime and risk recommendations.

## Run
```bash
python -m services.api_gateway.main
```

Environment variables (prefix `API_`):
- `DB_DSN` — database connection string.
