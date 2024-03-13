from typing import Any, Optional
from sqlmodel import Session
from sqlalchemy.exc import IntegrityError

from fastapi import logger
from app.api.exceptions.base import ImATeapotException
from app.api.exceptions.users import (
    UserAlreadyExistsException,
    UserNotFoundException,
)
from app.api.models.users import User
from app.api.repositories.users import UserRepository


class UsersService:
    """
    Class to handle all business related operations on `User` model

    Attributes:
        model: User
    """

    model = User

    @classmethod
    def get_one(
        cls, filter: Optional[dict] = None, db: Optional[Session] = None
    ) -> User:
        try:
            if filter:
                filter_dict = filter.copy()
                filter = [getattr(cls.model, k) == v for k, v in filter.items()]
            user = UserRepository.get(filter=filter, db=db).one_or_none()
            if not user:
                filter = filter_dict
                return UserNotFoundException(identifier=filter).response()
            else:
                return user
        except Exception as e:
            logger.logger.exception(e)
            return ImATeapotException().response()

    @classmethod
    def get_all(
        cls, filter: Optional[dict] = None, db: Optional[Session] = None
    ) -> list[User]:
        try:
            if filter:
                filter_dict = filter.copy()
                filter = [getattr(cls.model, k) == v for k, v in filter.items()]
            users = UserRepository.get(filter=filter, db=db).all()
            if not users:
                filter = filter_dict
                return UserNotFoundException(identifier=filter).response()
            else:
                return users
        except Exception as e:
            logger.logger.exception(e)
            return ImATeapotException().response()

    @classmethod
    def create(cls, data: dict = None, db: Optional[Session] = None):
        """Create a new `User` instance in the database"""
        try:
            user = UserRepository.create(data=data, db=db)
            return user
        except IntegrityError as e:
            logger.logger.exception(e)
            return UserAlreadyExistsException(
                identifier={"email": data["email"]}
            ).response()
        except Exception as e:
            logger.logger.exception(e)
            return ImATeapotException().response()

    @classmethod
    def update(
        cls,
        filter: dict[str, Any] = None,
        data: dict[str, Any] = None,
        db: Optional[Session] = None,
    ):
        try:
            if filter:
                filter_dict = filter.copy()
                filter = [getattr(cls.model, k) == v for k, v in filter.items()]
            user = UserRepository.update(filter=filter, data=data, db=db)
            if not user:
                filter = filter_dict
                return UserNotFoundException(identifier=filter).response()
            return user
        except Exception as e:
            logger.logger.exception(e)
            return ImATeapotException().response()

    @classmethod
    def delete(cls, filter: dict[str, Any] = None, db: Optional[Session] = None):
        try:
            if filter:
                filter_dict = filter.copy()
                filter = [getattr(cls.model, k) == v for k, v in filter.items()]
            deleted = UserRepository.delete(filter=filter, db=db)
            if not deleted:
                filter = filter_dict
                return UserNotFoundException(identifier=filter).response()
            return None
        except Exception as e:
            logger.logger.exception(e)
            return ImATeapotException().response()
