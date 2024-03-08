import os
import asyncio
import pytest
from sqlalchemy import create_engine
from sqlmodel import Session
from httpx import AsyncClient

from app.api.models.users import User
from app.settings import settings


fake_users = {
    "darth": User(
        id=1,
        first_name="Darth",
        last_name="Vader",
        email="jointhedarkside@empire.com",
        password=User.hash_password("Anakin"),
        active=True,
        superuser=True,
    ),
    "luke": User(
        id=2,
        first_name="Luke",
        last_name="Skywalker",
        email="jointhelightside@rebels.com",
        password=User.hash_password("Father"),
        active=True,
        superuser=True,
    ),
}

@pytest.fixture(scope="function")
def app_with_db():
    from app.main import app
    from app.api.db import SQLBaseModel, get_session
    engine = create_engine(
        settings.sql_alchemy_database_url,
        connect_args={"check_same_thread": False},
    )

    def override_get_session():
        with Session(engine, autoflush=True) as session:
            yield session


    app.dependency_overrides[get_session] = override_get_session

    SQLBaseModel.metadata.create_all(bind=engine)
    
    with Session(engine) as session:
        for user in fake_users.values():
            session.add(user)
        session.commit()
   
    yield app

    app.dependency_overrides = {}
    SQLBaseModel.metadata.drop_all(bind=engine)
    os.remove(settings.sql_alchemy_database_url.split("/")[-1])


@pytest.fixture
def app_without_db(app_with_db):
    from app.api.db import get_session
    engine = create_engine(
        settings.sql_alchemy_database_url,
        connect_args={"check_same_thread": False},
    )
    
    def override_get_session():
        with Session(engine.dispose(), autoflush=True) as session:
            yield session


    app_with_db.dependency_overrides[get_session] = override_get_session

    yield app_with_db


@pytest.fixture
def app_with_db_and_jwt(app_with_db):
    from app.api.auth import validate_access_token, token_dependency
    from app.api.schemas.token import TokenData
    def override_token_dependency():
        return 
    def override_jwt_dependency(fake_jwt):
        print(fake_jwt)
        return TokenData(id=1, email="jointhedarkside@empire.com")
    app_with_db.dependency_overrides[validate_access_token] = override_jwt_dependency
    app_with_db.dependency_overrides[token_dependency] = override_token_dependency
    yield app_with_db


# @pytest.fixture(scope="session")
# def event_loop():
#     loop = asyncio.new_event_loop()
#     yield loop
#     loop.close()

# @pytest.fixture(scope="function")
# async def client(app_with_db):
#     async with AsyncClient(app=app_with_db) as c:
#         yield c