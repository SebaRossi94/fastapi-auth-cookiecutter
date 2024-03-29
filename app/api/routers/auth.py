from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from app.api.schemas.token import TokenSchema
from app.api.models.users import User
from app.api.db import get_session_dependency
from app.api.auth import create_access_token

auth_router = APIRouter(prefix="/auth", tags=["auth"])


@auth_router.post("/token", response_model=TokenSchema)
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: get_session_dependency,
):
    user = User.authenticate_user(
        email=form_data.username, password=form_data.password, db=db
    )
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials"
        )
    else:
        token = create_access_token(user.email, user.id)
        return TokenSchema(access_token=token, token_type="bearer")
