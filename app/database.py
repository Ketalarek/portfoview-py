# app/database.py
from pathlib import Path

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

# umístění DB souboru: ./data/app.db
DB_DIR = Path(__file__).resolve().parents[1] / "data"
DB_DIR.mkdir(exist_ok=True)
SQLALCHEMY_DATABASE_URL = f"sqlite:///{DB_DIR / 'app.db'}"

# connect_args je potřeba pro SQLite v jednovláknové konfiguraci
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
