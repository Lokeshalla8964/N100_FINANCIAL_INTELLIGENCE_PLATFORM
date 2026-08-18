from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)


def test_root():
    response = client.get("/")
    assert response.status_code == 200


def test_health():
    response = client.get("/health")
    assert response.status_code == 200


def test_companies():
    response = client.get("/api/v1/companies")
    assert response.status_code == 200


def test_all_ratios():
    response = client.get("/api/v1/ratios/")
    assert response.status_code == 200


def test_health():
    response = client.get("/health")
    assert response.status_code == 200


def test_get_companies():
    response = client.get("/api/v1/companies")
    assert response.status_code == 200


def test_get_company_profile():
    response = client.get("/api/v1/companies/1/profile")
    assert response.status_code in [200, 404]


def test_get_all_ratios():
    response = client.get("/api/v1/ratios")
    assert response.status_code == 200


def test_get_company_ratios():
    response = client.get("/api/v1/ratios/1")
    assert response.status_code in [200, 404]