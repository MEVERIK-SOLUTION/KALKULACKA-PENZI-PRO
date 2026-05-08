import signal
import subprocess
import sys
import time
from pathlib import Path

import httpx
import pytest


@pytest.fixture(scope="session")
def api_server():
    proc = subprocess.Popen(
        [sys.executable, "-m", "uvicorn", "api.main:app", "--host", "127.0.0.1", "--port", "8765"],
        cwd=Path(__file__).parent.parent,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    for _ in range(20):
        try:
            httpx.get("http://127.0.0.1:8765/", timeout=1)
            break
        except Exception:
            time.sleep(0.5)
    else:
        proc.kill()
        raise RuntimeError("API server failed to start")
    yield
    proc.send_signal(signal.SIGTERM)
    proc.wait()


@pytest.mark.e2e
class TestDashboardE2E:
    def test_dashboard_loads(self, page, api_server):
        page.goto("http://127.0.0.1:8765/dashboard")
        assert page.title() is not None
        assert page.locator("h1").is_visible()

    def test_api_root_response(self, page, api_server):
        resp = page.goto("http://127.0.0.1:8765/")
        assert resp.ok
        body = resp.json()
        assert "endpoints" in body


@pytest.mark.e2e
class TestPensionCalculationE2E:
    def test_calculate_pension_button(self, api_server):
        import httpx
        resp = httpx.post("http://127.0.0.1:8765/calculate-pension", json={
            "annual_incomes": [38000 * 12],
            "coefficients": [1.0581],
            "insurance_years": 45,
            "excluded_days": 0,
        })
        assert resp.status_code == 200
        data = resp.json()
        assert "pension_amount" in data
        assert data["pension_amount"] > 0

    def test_invalid_request(self, api_server):
        import httpx
        resp = httpx.post("http://127.0.0.1:8765/calculate-pension", json={})
        assert resp.status_code == 422
