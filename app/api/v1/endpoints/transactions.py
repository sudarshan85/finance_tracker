from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.crud import transaction as transaction_crud
from app.schemas.transaction import Transaction, TransactionCreate, TransactionUpdate
from app.db.database import get_db
from app.schemas.query import QueryParams, PaginatedResponse

router = APIRouter()

@router.post("/", response_model=Transaction)
def create_transaction(transaction: TransactionCreate, db: Session = Depends(get_db)):
    return transaction_crud.create_transaction(db=db, transaction=transaction)

@router.post("/query", response_model=PaginatedResponse[Transaction])
def query_transactions(query_params: QueryParams, db: Session = Depends(get_db)):
    transactions, total = transaction_crud.get_transactions(db, query_params)
    return PaginatedResponse(
        items=transactions,
        total=total,
        page=query_params.skip // query_params.limit + 1,
        size=query_params.limit
    )

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