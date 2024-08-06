from sqlalchemy.orm import Session
from app.db.models import Account
from app.schemas.account import AccountCreate, AccountUpdate
from app.schemas.query import QueryParams
from app.utils.query import apply_filters, apply_sorting

def get_account(db: Session, account_id: int):
    return db.query(Account).filter(Account.id == account_id).first()

def get_accounts(db: Session, query_params: QueryParams):
    query = db.query(Account)
    
    if query_params.filters:
        query = apply_filters(query, Account, query_params.filters)
    
    if query_params.sort:
        query = apply_sorting(query, Account, query_params.sort)
    
    total = query.count()
    accounts = query.offset(query_params.skip).limit(query_params.limit).all()
    
    return accounts, total

def create_account(db: Session, account: AccountCreate):
    db_account = Account(**account.model_dump())
    db.add(db_account)
    db.commit()
    db.refresh(db_account)
    return db_account

def update_account(db: Session, account_id: int, account: AccountUpdate):
    db_account = get_account(db, account_id)
    if db_account:
        update_data = account.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_account, key, value)
        db.commit()
        db.refresh(db_account)
    return db_account

def delete_account(db: Session, account_id: int):
    db_account = get_account(db, account_id)
    if db_account:
        db.delete(db_account)
        db.commit()
    return db_account