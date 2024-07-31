from fastapi import FastAPI
from app.core.config import settings

app = FastAPI(title=settings.app_name, debug=settings.debug)

@app.get("/")
async def root():
    return {
        "message": f"Welcome to the {settings.app_name} API",
        "environment": settings.environment,
        "debug_mode": settings.debug
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy", "environment": settings.environment}