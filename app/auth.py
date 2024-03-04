from typing import Annotated
from fastapi import Depends
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")

token_dependency = Annotated[str, Depends(oauth2_scheme)]

bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")