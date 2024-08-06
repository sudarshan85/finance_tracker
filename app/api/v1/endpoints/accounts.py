from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Tuple

from app.crud import account as account_crud
from app.schemas.account import Account, AccountCreate, AccountUpdate
from app.db.database import get_db
from app.schemas.query import QueryParams, PaginatedResponse

router = APIRouter()

@router.post("/", response_model=Account)
def create_account(account: AccountCreate, db: Session = Depends(get_db)):
    return account_crud.create_account(db=db, account=account)

@router.post("/query", response_model=PaginatedResponse[Account])
def query_accounts(query_params: QueryParams, db: Session = Depends(get_db)):
    accounts, total = account_crud.get_accounts(db, query_params)
    return PaginatedResponse(
        items=accounts,
        total=total,
        page=query_params.skip // query_params.limit + 1,
        size=query_params.limit
    )

@router.get("/{account_id}", response_model=Account)
def read_account(account_id: int, db: Session = Depends(get_db)):
    db_account = account_crud.get_account(db, account_id=account_id)
    if db_account is None:
        raise HTTPException(status_code=404, detail="Account not found")
    return db_account

@router.put("/{account_id}", response_model=Account)
def update_account(account_id: int, account: AccountUpdate, db: Session = Depends(get_db)):
    db_account = account_crud.update_account(db, account_id=account_id, account=account)
    if db_account is None:
        raise HTTPException(status_code=404, detail="Account not found")
    return db_account

@router.delete("/{account_id}", response_model=Account)
def delete_account(account_id: int, db: Session = Depends(get_db)):
    db_account = account_crud.delete_account(db, account_id=account_id)
    if db_account is None:
        raise HTTPException(status_code=404, detail="Account not found")
    return db_account