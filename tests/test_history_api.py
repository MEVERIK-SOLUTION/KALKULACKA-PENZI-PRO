import httpx
import pytest
from httpx import ASGITransport


@pytest.fixture
def event_loop():
    import asyncio
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()


@pytest.fixture
async def async_client():
    from api.main import app
    transport = ASGITransport(app=app)
    async with httpx.AsyncClient(transport=transport, base_url="http://test") as client:
        yield client


@pytest.mark.asyncio
class TestHistoryAPI:
    async def test_list_empty(self, async_client):
        resp = await async_client.get("/history/")
        assert resp.status_code == 200
        assert resp.json() == []

    async def test_save_and_retrieve(self, async_client):
        payload = {
            "calc_type": "pension_test",
            "input_data": {"annual_income": 500000, "years": 45},
            "result": {"pension_amount": 20000, "ovz": 38000},
            "ovz": 38000.0,
            "pension_amount": 20000.0,
            "insurance_years": 45.0,
        }
        resp = await async_client.post("/history/", json=payload)
        assert resp.status_code == 201
        data = resp.json()
        assert data["calc_type"] == "pension_test"
        assert data["ovz"] == 38000.0
        assert data["pension_amount"] == 20000.0
        assert data["client_ip"] is not None
        record_id = data["id"]

        resp2 = await async_client.get(f"/history/{record_id}")
        assert resp2.status_code == 200
        assert resp2.json()["id"] == record_id

    async def test_list_filter_by_type(self, async_client):
        await async_client.post("/history/", json={"calc_type": "a", "input_data": {}, "result": {}})
        await async_client.post("/history/", json={"calc_type": "a", "input_data": {}, "result": {}})
        await async_client.post("/history/", json={"calc_type": "b", "input_data": {}, "result": {}})

        resp = await async_client.get("/history/?calc_type=a")
        data = resp.json()
        assert all(r["calc_type"] == "a" for r in data)

    async def test_get_nonexistent(self, async_client):
        resp = await async_client.get("/history/99999")
        assert resp.status_code == 404

    async def test_delete(self, async_client):
        resp = await async_client.post("/history/", json={"calc_type": "del_test", "input_data": {}, "result": {}})
        record_id = resp.json()["id"]

        resp_del = await async_client.delete(f"/history/{record_id}")
        assert resp_del.status_code == 204

        resp_get = await async_client.get(f"/history/{record_id}")
        assert resp_get.status_code == 404

    async def test_delete_nonexistent(self, async_client):
        resp = await async_client.delete("/history/99999")
        assert resp.status_code == 404
