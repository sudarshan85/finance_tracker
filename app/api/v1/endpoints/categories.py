from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.crud import category as category_crud
from app.schemas.category import Category, CategoryCreate, CategoryUpdate
from app.db.database import get_db
from app.schemas.query import QueryParams, PaginatedResponse

router = APIRouter()

@router.post("/", response_model=Category)
def create_category(category: CategoryCreate, db: Session = Depends(get_db)):
    return category_crud.create_category(db=db, category=category)

@router.post("/query", response_model=PaginatedResponse[Category])
def query_categories(query_params: QueryParams, db: Session = Depends(get_db)):
    categories, total = category_crud.get_categories(db, query_params)
    return PaginatedResponse(
        items=categories,
        total=total,
        page=query_params.skip // query_params.limit + 1,
        size=query_params.limit
    )

@router.get("/{category_id}", response_model=Category)
def read_category(category_id: int, db: Session = Depends(get_db)):
    db_category = category_crud.get_category(db, category_id=category_id)
    if db_category is None:
        raise HTTPException(status_code=404, detail="Category not found")
    return db_category

@router.put("/{category_id}", response_model=Category)
def update_category(category_id: int, category: CategoryUpdate, db: Session = Depends(get_db)):
    db_category = category_crud.update_category(db, category_id=category_id, category=category)
    if db_category is None:
        raise HTTPException(status_code=404, detail="Category not found")
    return db_category

@router.delete("/{category_id}", response_model=Category)
def delete_category(category_id: int, db: Session = Depends(get_db)):
    db_category = category_crud.delete_category(db, category_id=category_id)
    if db_category is None:
        raise HTTPException(status_code=404, detail="Category not found")
    return db_category