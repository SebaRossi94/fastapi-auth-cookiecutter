from pydantic import EmailStr
from sqlalchemy import Boolean, Column, Integer, String
from sqlmodel import Field, select
from app.db import SQLBaseModelAudit, get_session_dependency
from app.auth import bcrypt_context

class User(SQLBaseModelAudit, table=True):
    id: int = Field(sa_column=Column(Integer, nullable=False, primary_key=True))
    first_name: str = Field(sa_column=Column(String(128), nullable=True))
    last_name: str = Field(sa_column=Column(String(128), nullable=True))
    email: EmailStr = Field(sa_column=Column(String(), unique=True, index=True))
    password: str = Field(sa_column=Column(String(128), nullable=False))
    active: bool = Field(sa_column=Column(Boolean, nullable=False, default=True))
    superuser: bool = Field(sa_column=Column(Boolean, nullable=False, default=True))

    @classmethod
    def hash_password(cls, password: str):
        return bcrypt_context.hash(password)
    
    @classmethod
    def verify_password(cls, password: str, hashed_password: str):
        return bcrypt_context.verify(password, hashed_password)
    
    @classmethod
    def authenticate_user(cls, email: str, password: str, db: get_session_dependency):
        user = db.exec(select(cls).where(cls.email == email)).first()
        if not user or not cls.verify_password(password, user.password):
            return False
        else:
            return user