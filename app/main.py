from fastapi import FastAPI
from app.api.routers import main_router
from app.settings import settings_dependency
from app.auth import token_dependency

app = FastAPI()

app.include_router(main_router)

@app.get("/", tags=["test"])
async def home(settings: settings_dependency, token: token_dependency):
    return {
        "Welcome": "Auth cookiecutter!",
        "settings": settings.__dict__,
        "token": token
    }
