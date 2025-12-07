"""Risk policy application."""
from __future__ import annotations

import yaml

from services.ingest_market.models import RegimeState, RiskRecommendation


class RiskPolicy:
    def __init__(self, policy_path: str):
        with open(policy_path, "r", encoding="utf-8") as f:
            self.policy = yaml.safe_load(f)

    def recommend(self, regime: RegimeState) -> RiskRecommendation:
        state_policy = self.policy.get(regime.risk_state)
        if not state_policy:
            raise ValueError(f"no policy for risk state {regime.risk_state}")
        return RiskRecommendation(
            ts=regime.ts,
            regime_ref_id=regime.id,
            gross_leverage_target=state_policy["gross_leverage_target"],
            net_beta_cap=state_policy["net_beta_cap"],
            altcoin_exposure_cap=state_policy["altcoin_exposure_cap"],
            enable_counterbook=state_policy.get("enable_counterbook", False),
            notes=state_policy.get("notes"),
        )
