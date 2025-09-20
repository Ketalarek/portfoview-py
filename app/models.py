# app/models.py
import enum
from datetime import UTC, datetime

from sqlalchemy import Column, DateTime, Enum, Float, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.database import Base


class AssetType(str, enum.Enum):
    stock = "stock"
    etf = "etf"
    crypto = "crypto"


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, nullable=False)

    transactions = relationship("Transaction", back_populates="user")


class Symbol(Base):
    __tablename__ = "symbols"

    id = Column(Integer, primary_key=True, index=True)
    ticker = Column(String, unique=True, nullable=False)
    asset_type = Column(Enum(AssetType), nullable=False)

    transactions = relationship("Transaction", back_populates="symbol")


class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    symbol_id = Column(Integer, ForeignKey("symbols.id"), nullable=False)
    quantity = Column(Float, nullable=False)
    price = Column(Float, nullable=False)
    date = Column(DateTime(timezone=True), nullable=False, default=lambda: datetime.now(UTC))

    user = relationship("User", back_populates="transactions")
    symbol = relationship("Symbol", back_populates="transactions")
