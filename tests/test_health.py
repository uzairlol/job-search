from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_health_endpoint() -> None:
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_companies_endpoint() -> None:
    response = client.get("/api/v1/companies")
    assert response.status_code == 200
    assert len(response.json()) >= 1
