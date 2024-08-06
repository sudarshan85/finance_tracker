from sqlalchemy.orm import Session
from app.db.models import Transaction
from app.schemas.transaction import TransactionCreate, TransactionUpdate, TransactionStatus
from app.schemas.query import QueryParams
from app.utils.query import apply_filters, apply_sorting

def get_transaction(db: Session, transaction_id: int):
    return db.query(Transaction).filter(Transaction.id == transaction_id).first()

def get_transactions(db: Session, query_params: QueryParams):
    query = db.query(Transaction)
    
    if query_params.filters:
        query = apply_filters(query, Transaction, query_params.filters)
    
    if query_params.sort:
        query = apply_sorting(query, Transaction, query_params.sort)
    
    total = query.count()
    transactions = query.offset(query_params.skip).limit(query_params.limit).all()
    
    return transactions, total

def create_transaction(db: Session, transaction: TransactionCreate):
    db_transaction = Transaction(**transaction.model_dump())
    db.add(db_transaction)
    db.commit()
    db.refresh(db_transaction)
    return db_transaction

def update_transaction(db: Session, transaction_id: int, transaction: TransactionUpdate):
    db_transaction = get_transaction(db, transaction_id)
    if db_transaction:
        update_data = transaction.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_transaction, key, value)
        db.commit()
        db.refresh(db_transaction)
    return db_transaction

def delete_transaction(db: Session, transaction_id: int):
    db_transaction = get_transaction(db, transaction_id)
    if db_transaction:
        db.delete(db_transaction)
        db.commit()
    return db_transaction

def complete_transaction(db: Session, transaction_id: int):
    db_transaction = get_transaction(db, transaction_id)
    if db_transaction:
        db_transaction.status = TransactionStatus.COMPLETED
        db.commit()
        db.refresh(db_transaction)
    return db_transaction