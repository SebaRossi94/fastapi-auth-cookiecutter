from typing import Any
from pydantic import BaseModel, Field

__all__ = ("BaseError", "BaseIdentifiedError", "NotFoundError", "AlreadyExistsError", "ImATeapotError")

class BaseError(BaseModel):
    """Base class for error messages"""
    message: str = Field(description="Error message or description")

class BaseIdentifiedError(BaseError):
    identifier: Any = Field(description="Unique identifier which this error references to")

class NotFoundError(BaseIdentifiedError):
    pass

class AlreadyExistsError(BaseIdentifiedError):
    pass

class ImATeapotError(BaseError):
    pass