from sqlalchemy.orm import Session
from app.db.models import Category
from app.schemas.category import CategoryCreate, CategoryUpdate
from app.schemas.query import QueryParams
from app.utils.query import apply_filters, apply_sorting

def get_category(db: Session, category_id: int):
    return db.query(Category).filter(Category.id == category_id).first()

def get_categories(db: Session, query_params: QueryParams):
    query = db.query(Category)
    
    if query_params.filters:
        query = apply_filters(query, Category, query_params.filters)
    
    if query_params.sort:
        query = apply_sorting(query, Category, query_params.sort)
    
    total = query.count()
    categories = query.offset(query_params.skip).limit(query_params.limit).all()
    
    return categories, total

def create_category(db: Session, category: CategoryCreate):
    db_category = Category(**category.model_dump())
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category

def update_category(db: Session, category_id: int, category: CategoryUpdate):
    db_category = get_category(db, category_id)
    if db_category:
        update_data = category.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_category, key, value)
        db.commit()
        db.refresh(db_category)
    return db_category

def delete_category(db: Session, category_id: int):
    db_category = get_category(db, category_id)
    if db_category:
        db.delete(db_category)
        db.commit()
    return db_category