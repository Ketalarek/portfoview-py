from app import models
from app.database import SessionLocal, engine


def run_seed():
    session = SessionLocal()
    try:
        # vyčisti pro opakovaný běh
        session.query(models.Transaction).delete()
        session.query(models.Symbol).delete()
        session.query(models.User).delete()

        # user
        user = models.User(username="demo")
        session.add(user)

        # symbols
        aapl = models.Symbol(ticker="AAPL", asset_type=models.AssetType.stock)
        vwce = models.Symbol(ticker="VWCE", asset_type=models.AssetType.etf)
        session.add_all([aapl, vwce])

        session.flush()  # aby se vygenerovala id

        # transactions
        t1 = models.Transaction(user_id=user.id, symbol_id=aapl.id, quantity=10, price=150)
        t2 = models.Transaction(user_id=user.id, symbol_id=vwce.id, quantity=5, price=100)
        session.add_all([t1, t2])

        session.commit()
        print("Seed OK")
    finally:
        session.close()


if __name__ == "__main__":
    models.Base.metadata.create_all(bind=engine)  # jistota
    run_seed()
