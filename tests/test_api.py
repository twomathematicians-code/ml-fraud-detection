import pytest
from httpx import ASGITransport, AsyncClient
from src.api.main import app

@pytest.fixture
async def client():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac

@pytest.mark.asyncio
async def test_health_check(client):
    resp = await client.get("/api/v1/health")
    assert resp.status_code == 200
    data = resp.json()
    assert data["status"] == "healthy"
    assert "model" in data

@pytest.mark.asyncio
async def test_transaction_scoring(client):
    payload = {
        "transaction_id": "TX-TEST-00001", "amount": 450.00,
        "merchant_category": "retail", "customer_id": "C-1001",
        "device_fingerprint": "abc123", "ip_address": "10.0.0.1"
    }
    resp = await client.post("/api/v1/score/transaction", json=payload)
    assert resp.status_code == 200
    data = resp.json()
    assert 0 <= data["fraud_probability"] <= 1
    assert data["risk_level"] in ("low", "medium", "high", "critical")
    assert data["decision"] in ("allow", "flag", "block")

@pytest.mark.asyncio
async def test_batch_scoring(client):
    batch = {
        "transactions": [
            {"transaction_id": f"TX-BATCH-{i:04d}", "amount": 100.0 * i,
             "merchant_category": "retail", "customer_id": "C-1001",
             "device_fingerprint": "dev1", "ip_address": "10.0.0.1"}
            for i in range(1, 6)
        ]
    }
    resp = await client.post("/api/v1/score/batch", json=batch)
    assert resp.status_code == 200
    data = resp.json()
    assert data["total"] == 5
    assert len(data["results"]) == 5

@pytest.mark.asyncio
async def test_invalid_category(client):
    payload = {
        "transaction_id": "TX-INVALID", "amount": 50.0,
        "merchant_category": "invalid_cat", "customer_id": "C-1",
        "device_fingerprint": "x", "ip_address": "1.1.1.1"
    }
    resp = await client.post("/api/v1/score/transaction", json=payload)
    assert resp.status_code == 422

@pytest.mark.asyncio
async def test_dashboard_stats(client):
    resp = await client.get("/api/v1/stats/dashboard")
    assert resp.status_code == 200
    data = resp.json()
    assert "fraud_rate" in data
    assert "risk_distribution" in data

@pytest.mark.asyncio
async def test_alerts_endpoint(client):
    resp = await client.get("/api/v1/alerts/recent?limit=5")
    assert resp.status_code == 200
    assert isinstance(resp.json(), list)
