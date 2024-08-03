from sqlalchemy.orm import Session
from app.db.models import BudgetAllocation
from app.schemas.budget_allocation import BudgetAllocationCreate, BudgetAllocationUpdate

def get_budget_allocation(db: Session, budget_allocation_id: int):
    return db.query(BudgetAllocation).filter(BudgetAllocation.id == budget_allocation_id).first()

def get_budget_allocations(db: Session, skip: int = 0, limit: int = 100):
    return db.query(BudgetAllocation).offset(skip).limit(limit).all()

def create_budget_allocation(db: Session, budget_allocation: BudgetAllocationCreate):
    db_budget_allocation = BudgetAllocation(**budget_allocation.dict())
    db.add(db_budget_allocation)
    db.commit()
    db.refresh(db_budget_allocation)
    return db_budget_allocation

def update_budget_allocation(db: Session, budget_allocation_id: int, budget_allocation: BudgetAllocationUpdate):
    db_budget_allocation = get_budget_allocation(db, budget_allocation_id)
    if db_budget_allocation:
        update_data = budget_allocation.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_budget_allocation, key, value)
        db.commit()
        db.refresh(db_budget_allocation)
    return db_budget_allocation

def delete_budget_allocation(db: Session, budget_allocation_id: int):
    db_budget_allocation = get_budget_allocation(db, budget_allocation_id)
    if db_budget_allocation:
        db.delete(db_budget_allocation)
        db.commit()
    return db_budget_allocation
