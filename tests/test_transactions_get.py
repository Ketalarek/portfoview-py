import subprocess

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_get_transactions_returns_seed_data():
    # seedneme DB před testem
    subprocess.run(["python", "-m", "app.seed"], check=True)

    resp = client.get("/api/transactions")
    assert resp.status_code == 200

    data = resp.json()
    assert isinstance(data, list)
    assert len(data) >= 2

    first = data[0]
    assert {"id", "user_id", "symbol_id", "quantity", "price", "date"} <= set(first.keys())
