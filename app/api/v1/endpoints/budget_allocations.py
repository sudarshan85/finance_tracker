from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.crud import budget_allocation as budget_allocation_crud
from app.schemas.budget_allocation import BudgetAllocation, BudgetAllocationCreate, BudgetAllocationUpdate
from app.db.database import get_db

router = APIRouter()

@router.post("/", response_model=BudgetAllocation)
def create_budget_allocation(budget_allocation: BudgetAllocationCreate, db: Session = Depends(get_db)):
    return budget_allocation_crud.create_budget_allocation(db=db, budget_allocation=budget_allocation)

@router.get("/", response_model=List[BudgetAllocation])
def read_budget_allocations(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    budget_allocations = budget_allocation_crud.get_budget_allocations(db, skip=skip, limit=limit)
    return budget_allocations

@router.get("/{budget_allocation_id}", response_model=BudgetAllocation)
def read_budget_allocation(budget_allocation_id: int, db: Session = Depends(get_db)):
    db_budget_allocation = budget_allocation_crud.get_budget_allocation(db, budget_allocation_id=budget_allocation_id)
    if db_budget_allocation is None:
        raise HTTPException(status_code=404, detail="Budget allocation not found")
    return db_budget_allocation

@router.put("/{budget_allocation_id}", response_model=BudgetAllocation)
def update_budget_allocation(budget_allocation_id: int, budget_allocation: BudgetAllocationUpdate, db: Session = Depends(get_db)):
    db_budget_allocation = budget_allocation_crud.update_budget_allocation(db, budget_allocation_id=budget_allocation_id, budget_allocation=budget_allocation)
    if db_budget_allocation is None:
        raise HTTPException(status_code=404, detail="Budget allocation not found")
    return db_budget_allocation

@router.delete("/{budget_allocation_id}", response_model=BudgetAllocation)
def delete_budget_allocation(budget_allocation_id: int, db: Session = Depends(get_db)):
    db_budget_allocation = budget_allocation_crud.delete_budget_allocation(db, budget_allocation_id=budget_allocation_id)
    if db_budget_allocation is None:
        raise HTTPException(status_code=404, detail="Budget allocation not found")
    return db_budget_allocation
