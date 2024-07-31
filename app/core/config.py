from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    app_name: str = "Finance Tracker"
    debug: bool = False
    database_url: str = "sqlite:///./test.db"
    environment: str = "dev"

    class Config:
        env_file = ".env"

@lru_cache()
def get_settings():
    return Settings()

settings = get_settings()