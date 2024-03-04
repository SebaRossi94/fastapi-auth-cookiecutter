from datetime import datetime, timedelta
from pydantic import BaseModel
from jose import jwt

from app.settings import Settings

class Token(BaseModel):
    access_token: str
    token_type: str

    @classmethod
    def create_access_token(cls, email: str, id: int, expires_in: int = Settings().jwt_expires_in):
        encode = {"sub": email, "id": id}
        expires = datetime.utcnow() + timedelta(minutes=expires_in)
        encode.update({"exp": expires})
        return jwt.encode(encode, key=Settings().jwt_secret_key, algorithm=Settings().jwt_algorithm)