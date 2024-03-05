from fastapi import Depends, HTTPException, logger
from fastapi.security import OAuth2PasswordBearer
from fastapi import status
from typing import Annotated
from passlib.context import CryptContext
from datetime import datetime, timedelta
from jose import JWTError, jwt
from app.api.schemas.token import TokenData

from app.settings import settings


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")

token_dependency = Annotated[str, Depends(oauth2_scheme)]

bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def create_access_token(email: str, id: int, expires_in: int = settings.jwt_expires_in):
    encode = {"sub": email, "id": id}
    expires = datetime.utcnow() + timedelta(minutes=expires_in)
    encode.update({"exp": expires})
    return jwt.encode(
        encode, key=settings.jwt_secret_key, algorithm=settings.jwt_algorithm
    )


def validate_access_token(token: token_dependency):
    try:
        token_payload = jwt.decode(
            token, key=settings.jwt_secret_key, algorithms=settings.jwt_algorithm
        )
        email = token_payload.get("sub")
        user_id = token_payload.get("id")
        if email is None or user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate user",
            )
        else:
            return TokenData(id=user_id, email=email)
    except JWTError as e:
        logger.logger.exception(e)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate user"
        )


jwt_dependency = Annotated[TokenData, Depends(validate_access_token)]
