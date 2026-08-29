from datetime import datetime, timezone

from services.ingest_market.models import RegimeState
from services.risk_daemon.policies import RiskPolicy


def test_policy_mapping(tmp_path):
    policy_file = tmp_path / "policy.yaml"
    policy_file.write_text(
        """
        risk_on:
          gross_leverage_target: 1.0
          net_beta_cap: 0.5
          altcoin_exposure_cap: 0.3
          enable_counterbook: false
        """
    )
    policy = RiskPolicy(str(policy_file))
    regime = RegimeState(
        id=1,
        ts=datetime.now(timezone.utc),
        symbol="BTCUSDT",
        vol_regime="calm",
        vol_value=0.1,
        corr_symbol=None,
        corr_value=None,
        risk_state="risk_on",
    )
    rec = policy.recommend(regime)
    assert float(rec.gross_leverage_target) == 1.0
