from pydantic import BaseModel
from typing import Optional

class BudgetAllocationBase(BaseModel):
    year: int
    month: int
    amount: float
    category_id: int

class BudgetAllocationCreate(BudgetAllocationBase):
    pass

class BudgetAllocationUpdate(BaseModel):
    year: Optional[int] = None
    month: Optional[int] = None
    amount: Optional[float] = None
    category_id: Optional[int] = None

class BudgetAllocation(BudgetAllocationBase):
    id: int

    class Config:
        orm_mode = True
