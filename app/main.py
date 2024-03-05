from fastapi import FastAPI, logger
from sqlalchemy import text
from app.api.routers import main_router
from app.settings import settings_dependency
from app.db import get_session_dependency

app = FastAPI()

app.include_router(main_router)


@app.get("/healthcheck", tags=["healthcheck"])
async def home(settings: settings_dependency, db: get_session_dependency):
    try:
        db_up = bool(db.exec(text("SELECT 1")).scalar())
    except Exception as e:
        logger.logger.error(e)
        db_up = False
    return {
        "application_up": True,
        "settings": settings.__dict__,
        "database_up": db_up
    }
