from typing import List, Optional
from fastapi import APIRouter, HTTPException, logger, status

from app.api.db import get_session_dependency
from app.api.auth import jwt_dependency
from app.api.exceptions.base import ImATeapotException, get_exception_responses
from app.api.exceptions.users import (
    UserAlreadyExistsException,
    UserNotFoundException,
)
from app.api.schemas.users import CreateUserSchema, ResponseUserSchema, UpdateUserSchema
from app.api.models.users import User
from app.api.services.users import UsersService

users_router = APIRouter(prefix="/users", tags=["users"])


@users_router.get(
    "/me",
    response_model=Optional[ResponseUserSchema],
    responses=get_exception_responses(UserNotFoundException, ImATeapotException),
)
def me(user_data: jwt_dependency, db: get_session_dependency):
    user = UsersService.get_one(filter=user_data.__dict__, db=db)
    return user


@users_router.get(
    "/all",
    response_model=List[ResponseUserSchema],
    responses=get_exception_responses(UserNotFoundException, ImATeapotException),
)
def get_all_users(db: get_session_dependency):
    users = UsersService.get_all(filter=None, db=db)
    return users


@users_router.get(
    "/{user_id}",
    response_model=ResponseUserSchema,
    responses=get_exception_responses(UserNotFoundException, ImATeapotException),
)
def get_user_by_id(user_id: int, db: get_session_dependency):
    filter = {"id": user_id}
    user = UsersService.get_one(filter=filter, db=db)
    return user


@users_router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=ResponseUserSchema,
    responses=get_exception_responses(UserAlreadyExistsException, ImATeapotException),
)
def create_user(db: get_session_dependency, user_data: CreateUserSchema):
    hashed_password = User.hash_password(user_data.password)
    user_data.password = hashed_password
    user = UsersService.create(data=user_data.__dict__, db=db)
    return user


@users_router.patch(
    "/{user_id}",
    response_model=ResponseUserSchema,
    responses=get_exception_responses(UserNotFoundException, ImATeapotException),
)
def update_user(user_id: int, user_data: UpdateUserSchema, db: get_session_dependency):
    filter = {"id": user_id}
    user = UsersService.update(filter=filter, data=user_data.__dict__, db=db)
    return user


@users_router.delete(
    "/{user_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    responses=get_exception_responses(UserNotFoundException, ImATeapotException),
)
def delete_user(user_id: int, db: get_session_dependency):
    filter = {"id": user_id}
    deleted = UsersService.delete(filter=filter, db=db)
    return deleted
