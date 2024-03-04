from pydantic import BaseModel, EmailStr


class CreateUserSchema(BaseModel):
    first_name: str | None = None
    last_name: str | None = None
    email: EmailStr
    password: str
    active: bool = True
    superuser: bool = False