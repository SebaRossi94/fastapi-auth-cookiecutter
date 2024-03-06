from time import time
from fastapi import APIRouter
from fastapi import logger
from sqlalchemy import text

from app.settings import settings_dependency
from app.api.db import get_session_dependency

health_router = APIRouter(prefix="/healthcheck", tags=["health"])


@health_router.get("/")
async def health(settings: settings_dependency, db: get_session_dependency):
    try:
        db_up = bool(db.exec(text("SELECT 1")).scalar())
    except Exception as e:
        logger.logger.error(e)
        db_up = False
    return {"application_up": True, "settings": settings.__dict__, "database_up": db_up}
