from sqlite3 import IntegrityError
from fastapi import APIRouter, HTTPException, status
from app.db import get_session_dependency
from app.api.schemas.users import CreateUserSchema
from app.api.models.users import User

users_router = APIRouter(prefix="/users", tags=["users"])


@users_router.post("/")
def create_user(db: get_session_dependency, user_data: CreateUserSchema):
    try:
        hashed_password = User.hash_password(user_data.password)
        user_data.password = hashed_password
        db_user = User(**user_data.__dict__)
        db.add(db_user)
        db.commit()
    except IntegrityError as e:
        print(e)
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User already exists")
    except Exception as e:
        print(e)
        raise HTTPException(status_code=status.HTTP_418_IM_A_TEAPOT, detail="Unhandled Error")