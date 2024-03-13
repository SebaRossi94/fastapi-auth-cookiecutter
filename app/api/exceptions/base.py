from typing import Type
from fastapi import status
from fastapi.responses import JSONResponse
from app.api.schemas.errors import (
    BaseError,
    BaseIdentifiedError,
    NotFoundError,
    ImATeapotError,
    AlreadyExistsError,
)


class BaseAPIException(Exception):
    """Base error for custom API exceptions"""

    message = "Generic error"
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    model = BaseError

    def __init__(self, **kwargs):
        kwargs.setdefault("message", self.message)
        self.message = kwargs.get("message")
        self.data = self.model(**kwargs)

    def __str__(self):
        return self.message

    def response(self):
        return JSONResponse(
            status_code=self.status_code, content=self.data.model_dump()
        )

    @classmethod
    def response_model(cls):
        return {cls.status_code: {"model": cls.model}}


class BaseIdentifiedException(BaseAPIException):
    """Base error for custom API exceptions that have an identifier"""

    message = "Identity error"
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    model = BaseIdentifiedError

    def __init__(self, identifier, **kwargs):
        super().__init__(identifier=identifier, **kwargs)


class NotFoundException(BaseIdentifiedException):
    message = "Identity not found"
    status_code = status.HTTP_404_NOT_FOUND
    model = NotFoundError


class AlreadyExistsException(BaseIdentifiedException):
    message = "Identity already exists"
    status_code = status.HTTP_409_CONFLICT
    model = AlreadyExistsError


class ImATeapotException(BaseAPIException):
    message = "Unhandled error"
    status_code = status.HTTP_418_IM_A_TEAPOT
    model = ImATeapotError


def get_exception_responses(*args: Type[BaseAPIException]) -> dict:
    """Given BaseAPIException classes, return a dict of responses used on FastAPI endpoint definition, with the format:
    {statuscode: schema, statuscode: schema, ...}"""
    responses = dict()
    for cls in args:
        responses.update(cls.response_model())
    return responses
