from fastapi import APIRouter
from .auth import auth_router
from .users import users_router

main_router = APIRouter()

main_router.include_router(auth_router)
main_router.include_router(users_router)
