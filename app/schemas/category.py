from pydantic import BaseModel
from typing import Optional

class CategoryBase(BaseModel):
    name: str
    type: str
    monthly_budget: float
    goal_amount: Optional[float] = None

class CategoryCreate(CategoryBase):
    pass

class CategoryUpdate(BaseModel):
    name: Optional[str] = None
    type: Optional[str] = None
    monthly_budget: Optional[float] = None
    goal_amount: Optional[float] = None

class Category(CategoryBase):
    id: int
    is_default: bool

    class Config:
        orm_mode = True