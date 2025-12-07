from fastapi.testclient import TestClient

from services.api_gateway.main import app


def test_health_live():
    client = TestClient(app)
    resp = client.get("/health/live")
    assert resp.status_code == 200
    assert resp.json()["status"] == "live"
