from datetime import datetime
from typing import Annotated
from fastapi import Depends
from sqlalchemy import Column, DateTime, create_engine, event
from sqlmodel import Field, SQLModel, Session

from .settings import settings


engine = create_engine(settings.sql_alchemy_database_url)


class SQLBaseModel(SQLModel):
    pass


class SQLBaseModelAudit(SQLBaseModel):
    created_at: datetime = Field(
        default_factory=datetime.utcnow,
        sa_column=Column(DateTime(timezone=True), default=datetime.utcnow),
    )
    updated_at: datetime = Field(
        default_factory=datetime.utcnow,
        sa_column=Column(DateTime(timezone=True), default=datetime.utcnow),
    )


@event.listens_for(SQLBaseModelAudit, "before_update", propagate=True)
def updated_at(mapper, connection, target):
    target.updated_at = datetime.utcnow()


def init_db():
    with engine.begin() as conn:
        conn.run_sync(SQLBaseModel.metadata.create_all)


def get_session():
    with Session(engine, autoflush=True) as session:
        with session.begin():
            yield session


def get_session_no_transaction():
    with Session(engine) as session:
        yield session


get_session_dependency = Annotated[Session, Depends(get_session)]
get_session_no_transaction_dependency = Annotated[
    Session, Depends(get_session_no_transaction)
]
