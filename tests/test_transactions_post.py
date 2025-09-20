# tests/test_transactions_post.py
import subprocess

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_post_transaction_happy_path():
    # seed – zajistí user_id=1, symbol_id=1
    subprocess.run(["python", "-m", "app.seed"], check=True)

    resp = client.post(
        "/api/transactions",
        json={"user_id": 1, "symbol_id": 1, "quantity": 7, "price": 123.45},
    )
    assert resp.status_code == 201
    data = resp.json()
    assert data["user_id"] == 1
    assert data["symbol_id"] == 1
    assert data["quantity"] == 7
    assert data["price"] == 123.45
    assert "id" in data and data["id"] > 0


def test_post_transaction_invalid_fk_returns_400():
    # seed pro jistotu (ale záměrně použijeme nesmyslné FK)
    subprocess.run(["python", "-m", "app.seed"], check=True)

    resp = client.post(
        "/api/transactions",
        json={"user_id": 9999, "symbol_id": 9999, "quantity": 1, "price": 1},
    )
    assert resp.status_code == 400
    assert "not found" in resp.json()["detail"].lower()
