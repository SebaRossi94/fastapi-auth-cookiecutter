import os
import pytest
from sqlalchemy import create_engine
from sqlmodel import Session
from app.api.db import SQLBaseModel, engine, get_session, get_session_no_transaction
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
    "luke":  User(
        id=2,
        first_name="Luke",
        last_name="Skywalker",
        email="jointhelightside@rebels.com",
        password=User.hash_password("Father"),
        active=True,
        superuser=True,
    ),
}

def create_users_data(engine):
    with Session(engine) as session:
        for user in fake_users.values():
            session.add(user)
        session.commit()

def init_test_db(_app):
    engine = create_engine(
        settings.sql_alchemy_database_url,
        connect_args={"check_same_thread": False},
    )
    def override_get_session():
        with Session(engine, autoflush=True) as session:
            with session.begin():
                yield session
    
    def override_get_session_no_transaction():
        with Session(engine) as session:
            yield session
    
    _app.dependency_overrides[get_session] = override_get_session
    _app.dependency_overrides[get_session_no_transaction] = override_get_session_no_transaction
    SQLBaseModel.metadata.create_all(bind=engine)
    create_users_data(engine)

def drop_test_db():
    engine.dispose()
    os.remove(settings.sql_alchemy_database_url.split("/")[-1])

@pytest.fixture
def app_with_db():
    from app.main import app
    init_test_db(app)
    yield app
    drop_test_db()

@pytest.fixture
def app_without_db():
    from app.main import app
    from app.api.db import get_session, get_session_no_transaction
    from sqlmodel import Session
    init_test_db(app)
    
    def override_get_session():
        with Session(engine.dispose(), autoflush=True) as session:
            with session.begin():
                yield session
    def override_get_session_no_transaction():
        with Session(engine.dispose()) as session:
            yield session

    app.dependency_overrides[get_session] = override_get_session
    app.dependency_overrides[get_session_no_transaction] = override_get_session_no_transaction
    yield app
    drop_test_db()
