from sqlalchemy.orm import Session
from app.db.models import Store
from app.schemas.store import StoreCreate, StoreUpdate

def get_store(db: Session, store_id: int):
    return db.query(Store).filter(Store.id == store_id).first()

def get_stores(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Store).offset(skip).limit(limit).all()

def create_store(db: Session, store: StoreCreate):
    db_store = Store(**store.dict())
    db.add(db_store)
    db.commit()
    db.refresh(db_store)
    return db_store

def update_store(db: Session, store_id: int, store: StoreUpdate):
    db_store = get_store(db, store_id)
    if db_store:
        update_data = store.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_store, key, value)
        db.commit()
        db.refresh(db_store)
    return db_store

def delete_store(db: Session, store_id: int):
    db_store = get_store(db, store_id)
    if db_store:
        db.delete(db_store)
        db.commit()
    return db_store
