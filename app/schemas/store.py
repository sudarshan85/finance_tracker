from pydantic import BaseModel
from typing import Optional

class StoreBase(BaseModel):
    name: str
    user_defined: bool = True

class StoreCreate(StoreBase):
    pass

class StoreUpdate(BaseModel):
    name: Optional[str] = None
    user_defined: Optional[bool] = None

class Store(StoreBase):
    id: int

    class Config:
        orm_mode = True
