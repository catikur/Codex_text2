CREATE EXTENSION IF NOT EXISTS timescaledb;

CREATE TABLE IF NOT EXISTS market_ohlcv (
    id SERIAL PRIMARY KEY,
    symbol TEXT NOT NULL,
    timeframe TEXT NOT NULL,
    ts TIMESTAMPTZ NOT NULL,
    open NUMERIC NOT NULL,
    high NUMERIC NOT NULL,
    low NUMERIC NOT NULL,
    close NUMERIC NOT NULL,
    volume NUMERIC NOT NULL,
    UNIQUE(symbol, timeframe, ts)
);

CREATE TABLE IF NOT EXISTS regime_state (
    id SERIAL PRIMARY KEY,
    ts TIMESTAMPTZ NOT NULL,
    symbol TEXT NOT NULL,
    vol_regime TEXT NOT NULL,
    vol_value NUMERIC NOT NULL,
    corr_symbol TEXT,
    corr_value NUMERIC,
    risk_state TEXT NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS risk_recommendation (
    id SERIAL PRIMARY KEY,
    ts TIMESTAMPTZ NOT NULL,
    regime_ref_id INTEGER REFERENCES regime_state(id),
    gross_leverage_target NUMERIC NOT NULL,
    net_beta_cap NUMERIC NOT NULL,
    altcoin_exposure_cap NUMERIC NOT NULL,
    enable_counterbook BOOLEAN NOT NULL DEFAULT FALSE,
    notes TEXT
);

SELECT create_hypertable('market_ohlcv', 'ts', if_not_exists => TRUE);
