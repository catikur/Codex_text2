.PHONY: up down tests migrate

up:
docker-compose up -d --build

down:
docker-compose down -v

migrate:
python -c "from common.db import run_init_sql; run_init_sql('infra/init_db.sql')"

tests:
pytest
