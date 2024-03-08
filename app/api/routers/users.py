from sqlite3 import IntegrityError
from typing import List, Optional
from fastapi import APIRouter, HTTPException, logger, status
from sqlmodel import select
from app.api.db import get_session_dependency
from app.api.auth import jwt_dependency
from app.api.repositories.users import UserRepository
from app.api.schemas.users import CreateUserSchema, ResponseUserSchema, UpdateUserSchema
from app.api.models.users import User

users_router = APIRouter(prefix="/users", tags=["users"])


@users_router.get("/me", response_model=Optional[ResponseUserSchema])
def me(user_data: jwt_dependency, db: get_session_dependency):
    user = UserRepository.get_one(filter=user_data.__dict__, db=db)
    return user


@users_router.get("/all", response_model=List[ResponseUserSchema])
def get_all_users(_: jwt_dependency, db: get_session_dependency):
    users = UserRepository.get_all(db=db)
    return users

@users_router.post("/", status_code=status.HTTP_201_CREATED, response_model=ResponseUserSchema)
def create_user(db: get_session_dependency, user_data: CreateUserSchema):
    hashed_password = User.hash_password(user_data.password)
    user_data.password = hashed_password
    user = UserRepository.create(data=user_data.__dict__, db=db)
    return user

@users_router.patch("/{user_id}", response_model=ResponseUserSchema)
def update_user(user_id: int, user_data: UpdateUserSchema, db: get_session_dependency):
    user = UserRepository.patch(user_id, data=user_data.__dict__, db=db)
    return user


@users_router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id: int, db: get_session_dependency):
    user = UserRepository.delete(user_id, db=db)
    return user