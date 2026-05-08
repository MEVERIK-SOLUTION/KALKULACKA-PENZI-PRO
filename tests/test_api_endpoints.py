import pytest
from fastapi.testclient import TestClient


@pytest.fixture(scope="session")
def client():
    from api.main import app
    return TestClient(app)


class TestRootEndpoint:
    def test_root_returns_info(self, client):
        resp = client.get("/")
        assert resp.status_code == 200
        data = resp.json()
        assert "message" in data
        assert "version" in data
        assert "endpoints" in data

    def test_root_has_all_endpoints(self, client):
        resp = client.get("/")
        endpoints = resp.json()["endpoints"]
        assert "dashboard" in endpoints
        assert "data_inflation" in endpoints
        assert "data_avg_wage" in endpoints
        assert "data_wage_growth" in endpoints
        assert "calculate_pension" in endpoints
        assert "calculate_ovz" in endpoints
        assert "calculate_early_retirement" in endpoints
        assert "resolve_paradox" in endpoints


class TestDashboardEndpoint:
    def test_dashboard_returns_html(self, client):
        resp = client.get("/dashboard")
        assert resp.status_code == 200
        assert "text/html" in resp.headers["content-type"]


class TestCalculateOVZ:
    def test_valid_request(self, client):
        resp = client.post("/calculate-ovz", json={
            "annual_incomes": [38000 * 12],
            "coefficients": [1.0581],
            "total_days": 365 * 45,
            "excluded_days": 0,
        })
        assert resp.status_code == 200
        data = resp.json()
        assert "ovz" in data
        assert data["ovz"] > 0

    def test_invalid_request(self, client):
        resp = client.post("/calculate-ovz", json={})
        assert resp.status_code == 422


class TestCalculatePension:
    def test_valid_request(self, client):
        resp = client.post("/calculate-pension", json={
            "annual_incomes": [38000 * 12],
            "coefficients": [1.0581],
            "insurance_years": 45,
            "excluded_days": 0,
        })
        assert resp.status_code == 200
        data = resp.json()
        assert "pension_amount" in data
        assert data["pension_amount"] > 0
        assert "ovz" in data
        assert "vz" in data

    def test_missing_fields(self, client):
        resp = client.post("/calculate-pension", json={
            "annual_incomes": [38000 * 12],
        })
        assert resp.status_code == 422


class TestEarlyRetirement:
    def test_valid_request(self, client):
        resp = client.post("/calculate-early-retirement", json={
            "pension_amount": 20000.0,
            "months_before": 12,
        })
        assert resp.status_code == 200
        data = resp.json()
        assert "reduced_pension" in data
        assert data["reduced_pension"] < 20000.0
        assert data["months_early"] == 12

    def test_zero_months(self, client):
        resp = client.post("/calculate-early-retirement", json={
            "pension_amount": 20000.0,
            "months_before": 0,
        })
        assert resp.status_code == 200
        data = resp.json()
        assert data["reduced_pension"] == 20000.0


class TestParadox:
    def test_valid_request(self, client):
        resp = client.post("/resolve-paradox", json={
            "annual_incomes": [38000 * 12],
            "coefficients": [1.0581],
            "total_days": 365 * 45,
            "substitute_days": 365,
        })
        assert resp.status_code == 200
        data = resp.json()
        assert "include_substitute_period" in data
        assert "recommendation" in data

    def test_recommendation_text(self, client):
        resp = client.post("/resolve-paradox", json={
            "annual_incomes": [35000 * 12],
            "coefficients": [1.0581],
            "total_days": 365 * 40,
            "substitute_days": 180,
        })
        data = resp.json()
        assert data["recommendation"] in ["Zahrnout náhradní dobu", "Vyloučit náhradní dobu"]
