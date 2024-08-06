from pydantic import BaseModel
from typing import List, Optional, Any, Union, Generic, TypeVar
from datetime import date, datetime

T = TypeVar('T')

class DateRange(BaseModel):
    start: Union[date, datetime]
    end: Union[date, datetime]

class FilterCondition(BaseModel):
    field: str
    operator: str
    value: Any
    data_type: str  # 'string', 'number', 'date', 'boolean', 'enum'

class SortOrder(BaseModel):
    field: str
    direction: str = "asc"

class QueryParams(BaseModel):
    filters: Optional[List[FilterCondition]] = None
    sort: Optional[List[SortOrder]] = None
    skip: int = 0
    limit: int = 100

class PaginatedResponse(BaseModel, Generic[T]):
    items: List[T]
    total: int
    page: int
    size: int