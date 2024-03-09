from datetime import datetime
from typing import Annotated
from fastapi import Depends
from sqlalchemy import Column, DateTime, create_engine, event
from sqlmodel import Field, SQLModel, Session

from app.settings import settings


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


def get_session():
    with Session(engine, autoflush=True) as session:
        yield session


get_session_dependency = Annotated[Session, Depends(get_session)]
