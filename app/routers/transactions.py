# app/routers/transactions.py
from fastapi import APIRouter, HTTPException, Response, status

from app import models
from app.database import SessionLocal
from app.schemas import TransactionCreate, TransactionRead

router = APIRouter(prefix="/api/transactions", tags=["transactions"])


@router.get("", response_model=list[TransactionRead])
def list_transactions():
    session = SessionLocal()
    try:
        return session.query(models.Transaction).order_by(models.Transaction.id).all()
    finally:
        session.close()


@router.post("", response_model=TransactionRead, status_code=status.HTTP_201_CREATED)
def create_transaction(payload: TransactionCreate):
    session = SessionLocal()
    try:
        # základní ověření FK, ať vrátíme 400 místo pádu DB
        if session.get(models.User, payload.user_id) is None:
            raise HTTPException(status_code=400, detail="User not found")
        if session.get(models.Symbol, payload.symbol_id) is None:
            raise HTTPException(status_code=400, detail="Symbol not found")

        tx = models.Transaction(**payload.model_dump())
        session.add(tx)
        session.commit()
        session.refresh(tx)
        return tx
    finally:
        session.close()


@router.delete("/{tx_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_transaction(tx_id: int):
    session = SessionLocal()
    try:
        tx = session.get(models.Transaction, tx_id)
        if tx is None:
            raise HTTPException(status_code=404, detail="Transaction not found")
        session.delete(tx)
        session.commit()
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    finally:
        session.close()
