from functools import lru_cache
import os
from typing import Annotated
from fastapi import Depends
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_env: str = os.environ.get("APP_ENV", "debug")
    sql_alchemy_database_url: str = os.environ.get(
        "SQL_ALCHEMY_DATABASE_URL", "sqlite:///./sql_app.db"
    )
    jwt_secret_key: str = os.environ.get("JWT_SECRET_KEY", "supersecretkey")
    jwt_algorithm: str = os.environ.get("JWT_ALGORITHM", "HS256")
    jwt_expires_in: int = os.environ.get("JWT_EXPIRES_IN", 20)


settings = Settings()


@lru_cache
def get_settings():
    return Settings()


settings_dependency = Annotated[BaseSettings, Depends(get_settings)]
