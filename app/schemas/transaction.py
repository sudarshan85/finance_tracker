from pydantic import BaseModel
from datetime import date
from typing import Optional

class TransactionBase(BaseModel):
    date: date
    amount: float
    description: str
    account_id: int
    category_id: int
    memo: Optional[str] = None
    store_id: Optional[int] = None

class TransactionCreate(TransactionBase):
    pass

class TransactionUpdate(BaseModel):
    date: Optional[date] = None
    amount: Optional[float] = None
    description: Optional[str] = None
    account_id: Optional[int] = None
    category_id: Optional[int] = None
    memo: Optional[str] = None
    store_id: Optional[int] = None

class Transaction(TransactionBase):
    id: int

    class Config:
        orm_mode = True
