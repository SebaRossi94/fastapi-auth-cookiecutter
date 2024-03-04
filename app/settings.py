from datetime import timedelta
from functools import lru_cache
from typing import Annotated
from fastapi import Depends
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    test_config: str = "My test Configuration"
    sql_alchemy_database_url: str = "sqlite:///./sql_app.db"
    jwt_secret_key: str = "supersecretkey"
    jwt_algorithm: str = "HS256"
    jwt_expires_in: int = 20

    model_config = SettingsConfigDict(env_file=".env")

@lru_cache
def get_settings():
    return Settings()

settings_dependency = Annotated[Settings, Depends(get_settings)]