from pydantic import BaseModel
from typing import Optional
from datetime import date

class AccountBase(BaseModel):
    name: str
    type: str
    balance: float

class AccountCreate(AccountBase):
    pass

class AccountUpdate(BaseModel):
    name: Optional[str] = None
    type: Optional[str] = None
    balance: Optional[float] = None
    last_reconciled: Optional[date] = None

class Account(AccountBase):
    id: int
    last_reconciled: Optional[date] = None

    class Config:
        orm_mode = True