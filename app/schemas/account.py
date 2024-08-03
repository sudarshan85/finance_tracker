from pydantic import BaseModel
from typing import Optional

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

class Account(AccountBase):
    id: int

    class Config:
        orm_mode = True