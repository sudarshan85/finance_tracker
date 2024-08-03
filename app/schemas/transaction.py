from pydantic import BaseModel
from datetime import date
from typing import Optional
from enum import Enum

class TransactionStatus(str, Enum):
    PENDING = "PENDING"
    COMPLETED = "COMPLETED"

class TransactionBase(BaseModel):
    date: date
    amount: float
    description: str
    account_id: int
    category_id: int
    store_id: Optional[int] = None
    status: TransactionStatus = TransactionStatus.PENDING

class TransactionCreate(TransactionBase):
    pass

class TransactionUpdate(BaseModel):
    date: Optional[date] = None
    amount: Optional[float] = None
    description: Optional[str] = None
    account_id: Optional[int] = None
    category_id: Optional[int] = None
    store_id: Optional[int] = None
    status: Optional[TransactionStatus] = None

class Transaction(TransactionBase):
    id: int

    class Config:
        orm_mode = True