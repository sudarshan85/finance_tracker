from pydantic import BaseModel
from datetime import date

class ReconciliationBase(BaseModel):
    date: date
    account_id: int

class ReconciliationCreate(ReconciliationBase):
    pass

class Reconciliation(ReconciliationBase):
    id: int

    class Config:
        orm_mode = True