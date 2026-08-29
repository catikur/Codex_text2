from services.regime_engine.correlation import rolling_correlation


def test_rolling_correlation_basic():
    a = [1, 2, 3, 4]
    b = [2, 3, 4, 5]
    corr = rolling_correlation(a, b)
    assert corr > 0.9
