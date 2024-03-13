from typing import Any, Optional
from sqlmodel import Session
from sqlalchemy.exc import IntegrityError

from fastapi import logger
from app.api.exceptions.users import (
    InvalidFilterParameterException,
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

        if filter:
            try:
                filter = [getattr(cls.model, k) == v for k, v in filter.items()]
            except AttributeError as e:
                logger.logger.exception(e)
                raise InvalidFilterParameterException()
        user = UserRepository.get(filter=filter, db=db).one_or_none()
        if not user:
            raise UserNotFoundException()
        else:
            return user

    @classmethod
    def get_all(
        cls, filter: Optional[dict] = None, db: Optional[Session] = None
    ) -> list[User]:
        if filter:
            try:
                filter = [getattr(cls.model, k) == v for k, v in filter.items()]
            except AttributeError as e:
                logger.logger.exception(e)
                raise InvalidFilterParameterException()
        users = UserRepository.get(filter=filter, db=db).all()
        if not users:
            raise UserNotFoundException()
        else:
            return users

    @classmethod
    def create(cls, data: dict = None, db: Optional[Session] = None):
        """Create a new `User` instance in the database"""
        try:
            user = UserRepository.create(data=data, db=db)
            return user
        except IntegrityError as e:
            logger.logger.exception(e)
            raise UserAlreadyExistsException()

    @classmethod
    def update(
        cls,
        filter: dict[str, Any] = None,
        data: dict[str, Any] = None,
        db: Optional[Session] = None,
    ):
        if filter:
            try:
                filter = [getattr(cls.model, k) == v for k, v in filter.items()]
            except AttributeError as e:
                logger.logger.exception(e)
                raise InvalidFilterParameterException()
        user = UserRepository.update(filter=filter, data=data, db=db)
        if not user:
            raise UserNotFoundException()
        return user

    @classmethod
    def delete(cls, filter: dict[str, Any] = None, db: Optional[Session] = None):
        if filter:
            try:
                filter = [getattr(cls.model, k) == v for k, v in filter.items()]
            except AttributeError as e:
                logger.logger.exception(e)
                raise InvalidFilterParameterException()
        deleted = UserRepository.delete(filter=filter, db=db)
        if not deleted:
            raise UserNotFoundException()
        return None
