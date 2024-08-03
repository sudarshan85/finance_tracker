from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from app.core.config import settings
from app.db.database import get_db
from app.api.v1.endpoints import categories, accounts, transactions, stores

app = FastAPI(title=settings.app_name, debug=settings.debug)

app.include_router(categories.router, prefix="/api/v1/categories", tags=["categories"])
app.include_router(accounts.router, prefix="/api/v1/accounts", tags=["accounts"])
app.include_router(transactions.router, prefix="/api/v1/transactions", tags=["transactions"])
app.include_router(stores.router, prefix="/api/v1/stores", tags=["stores"])

@app.get("/")
async def root(db: Session = Depends(get_db)):
    return {
        "message": f"Welcome to the {settings.app_name} API",
        "environment": settings.environment,
        "debug_mode": settings.debug
    }

@app.get("/health")
async def health_check(db: Session = Depends(get_db)):
    return {"status": "healthy", "environment": settings.environment}