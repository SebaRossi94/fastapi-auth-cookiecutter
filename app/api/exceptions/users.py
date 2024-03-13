from typing import Any
from fastapi import HTTPException, status

from app.api.exceptions.base import NotFoundException, AlreadyExistsException


class UserNotFoundException(NotFoundException):
    message = "User not found"


class UserAlreadyExistsException(AlreadyExistsException):
    message = "User already exists"

