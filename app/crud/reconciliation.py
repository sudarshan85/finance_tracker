from sqlalchemy.orm import Session
from app.db.models import Reconciliation, Account
from app.schemas.reconciliation import ReconciliationCreate

def create_reconciliation(db: Session, reconciliation: ReconciliationCreate):
    db_reconciliation = Reconciliation(**reconciliation.dict())
    db.add(db_reconciliation)
    
    # Update the account's last_reconciled date
    account = db.query(Account).filter(Account.id == reconciliation.account_id).first()
    if account:
        account.last_reconciled = reconciliation.date
    
    db.commit()
    db.refresh(db_reconciliation)
    return db_reconciliation

def get_last_reconciliation(db: Session, account_id: int):
    return db.query(Reconciliation).filter(Reconciliation.account_id == account_id).order_by(Reconciliation.date.desc()).first()