import subprocess

from app import models
from app.database import SessionLocal


def test_seed_inserts_data():
    # spusť seed skript
    subprocess.run(["python", "-m", "app.seed"], check=True)

    session = SessionLocal()
    try:
        users = session.query(models.User).all()
        symbols = session.query(models.Symbol).all()
        transactions = session.query(models.Transaction).all()

        assert len(users) == 1
        assert users[0].username == "demo"

        tickers = {s.ticker for s in symbols}
        assert tickers == {"AAPL", "VWCE"}

        assert len(transactions) == 2
        assert any(t.quantity == 10 and t.price == 150 for t in transactions)
        assert any(t.quantity == 5 and t.price == 100 for t in transactions)
    finally:
        session.close()
