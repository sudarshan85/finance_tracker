from pydantic_settings import BaseSettings
from functools import lru_cache
import os

class Settings(BaseSettings):
    app_name: str = "Finance Tracker"
    debug: bool = os.getenv("DEBUG", "False").lower() == "true"
    database_url: str = os.getenv("DATABASE_URL", "sqlite:///./finance_tracker.db")
    environment: str = os.getenv("ENVIRONMENT", "dev")

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

@lru_cache()
def get_settings():
    return Settings()

def reload_settings():
    if "get_settings" in globals():
        get_settings.cache_clear()
    return get_settings()

settings = get_settings()