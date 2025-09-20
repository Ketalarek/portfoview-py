# tests/test_transactions_delete.py
import subprocess

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_delete_transaction_happy_path():
    subprocess.run(["python", "-m", "app.seed"], check=True)
    # ověř že existuje id=1
    resp = client.get("/api/transactions")
    txs = resp.json()
    tx_id = txs[0]["id"]

    # smaž
    resp = client.delete(f"/api/transactions/{tx_id}")
    assert resp.status_code == 204

    # ověř že tam už není
    resp = client.get("/api/transactions")
    ids = [t["id"] for t in resp.json()]
    assert tx_id not in ids


def test_delete_transaction_not_found():
    subprocess.run(["python", "-m", "app.seed"], check=True)

    resp = client.delete("/api/transactions/99999")
    assert resp.status_code == 404
    assert "not found" in resp.json()["detail"].lower()
