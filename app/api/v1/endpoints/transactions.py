from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.crud import transaction as transaction_crud
from app.schemas.transaction import Transaction, TransactionCreate, TransactionUpdate, TransactionStatus
from app.db.database import get_db

router = APIRouter()

@router.post("/", response_model=Transaction)
def create_transaction(transaction: TransactionCreate, db: Session = Depends(get_db)):
    return transaction_crud.create_transaction(db=db, transaction=transaction)

@router.get("/", response_model=List[Transaction])
def read_transactions(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    transactions = transaction_crud.get_transactions(db, skip=skip, limit=limit)
    return transactions

@router.get("/{transaction_id}", response_model=Transaction)
def read_transaction(transaction_id: int, db: Session = Depends(get_db)):
    db_transaction = transaction_crud.get_transaction(db, transaction_id=transaction_id)
    if db_transaction is None:
        raise HTTPException(status_code=404, detail="Transaction not found")
    return db_transaction

@router.put("/{transaction_id}", response_model=Transaction)
def update_transaction(transaction_id: int, transaction: TransactionUpdate, db: Session = Depends(get_db)):
    db_transaction = transaction_crud.update_transaction(db, transaction_id=transaction_id, transaction=transaction)
    if db_transaction is None:
        raise HTTPException(status_code=404, detail="Transaction not found")
    return db_transaction

@router.delete("/{transaction_id}", response_model=Transaction)
def delete_transaction(transaction_id: int, db: Session = Depends(get_db)):
    db_transaction = transaction_crud.delete_transaction(db, transaction_id=transaction_id)
    if db_transaction is None:
        raise HTTPException(status_code=404, detail="Transaction not found")
    return db_transaction

@router.put("/{transaction_id}/complete", response_model=Transaction)
def complete_transaction(transaction_id: int, db: Session = Depends(get_db)):
    db_transaction = transaction_crud.complete_transaction(db, transaction_id=transaction_id)
    if db_transaction is None:
        raise HTTPException(status_code=404, detail="Transaction not found")
    return db_transaction