from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.crud import store as store_crud
from app.schemas.store import Store, StoreCreate, StoreUpdate
from app.db.database import get_db

router = APIRouter()

@router.post("/", response_model=Store)
def create_store(store: StoreCreate, db: Session = Depends(get_db)):
    return store_crud.create_store(db=db, store=store)

@router.get("/", response_model=List[Store])
def read_stores(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    stores = store_crud.get_stores(db, skip=skip, limit=limit)
    return stores

@router.get("/{store_id}", response_model=Store)
def read_store(store_id: int, db: Session = Depends(get_db)):
    db_store = store_crud.get_store(db, store_id=store_id)
    if db_store is None:
        raise HTTPException(status_code=404, detail="Store not found")
    return db_store

@router.put("/{store_id}", response_model=Store)
def update_store(store_id: int, store: StoreUpdate, db: Session = Depends(get_db)):
    db_store = store_crud.update_store(db, store_id=store_id, store=store)
    if db_store is None:
        raise HTTPException(status_code=404, detail="Store not found")
    return db_store

@router.delete("/{store_id}", response_model=Store)
def delete_store(store_id: int, db: Session = Depends(get_db)):
    db_store = store_crud.delete_store(db, store_id=store_id)
    if db_store is None:
        raise HTTPException(status_code=404, detail="Store not found")
    return db_store
