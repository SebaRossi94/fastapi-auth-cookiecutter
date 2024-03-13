from typing import Any
from fastapi import status


class UserNotFoundException(Exception):
    def __init__(
        self,
        status_code: status = status.HTTP_404_NOT_FOUND,
        detail: Any = "User not found",
    ):
        self.status_code = status_code
        self.detail = detail
        super().__init__()


class InvalidFilterParameterException(Exception):
    def __init__(
        self,
        status_code: status = status.HTTP_400_BAD_REQUEST,
        detail: Any = "Invalid filter parameter",
    ):
        self.status_code = status_code
        self.detail = detail
        super().__init__()


class UserAlreadyExistsException(Exception):
    def __init__(
        self,
        status_code: status = status.HTTP_409_CONFLICT,
        detail: Any = "User already exists",
    ):
        self.status_code = status_code
        self.detail = detail
        super().__init__()
