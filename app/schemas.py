# app/schemas.py
from datetime import datetime

from pydantic import BaseModel, ConfigDict


class TransactionRead(BaseModel):
    id: int
    user_id: int
    symbol_id: int
    quantity: float
    price: float
    date: datetime

    model_config = ConfigDict(from_attributes=True)  # Pydantic v2: ORM mode


class TransactionCreate(BaseModel):
    user_id: int
    symbol_id: int
    quantity: float
    price: float
    # date nechte vynechané → vezme se default z modelu (UTC now)
