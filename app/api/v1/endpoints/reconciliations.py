from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.crud import reconciliation as reconciliation_crud
from app.schemas.reconciliation import Reconciliation, ReconciliationCreate
from app.db.database import get_db

router = APIRouter()

@router.post("/", response_model=Reconciliation)
def create_reconciliation(reconciliation: ReconciliationCreate, db: Session = Depends(get_db)):
    return reconciliation_crud.create_reconciliation(db=db, reconciliation=reconciliation)

@router.get("/{account_id}/last", response_model=Reconciliation)
def get_last_reconciliation(account_id: int, db: Session = Depends(get_db)):
    db_reconciliation = reconciliation_crud.get_last_reconciliation(db, account_id=account_id)
    if db_reconciliation is None:
        raise HTTPException(status_code=404, detail="No reconciliation found for this account")
    return db_reconciliation