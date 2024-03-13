from typing import Any, Optional

from sqlalchemy.sql.elements import BinaryExpression
from sqlalchemy.engine.result import ScalarResult

from sqlmodel import Session, select


class BaseRepository:
    """
    Base class to handle all DB interactions

    Attributes:
        model: The model to be set to which the methods will execute DB operations
    """

    model = None

    @classmethod
    def get(
        cls,
        filter: Optional[list[BinaryExpression]] = None,
        db: Optional[Session] = None,
    ) -> ScalarResult:
        "Returns a `ScalarResult` of the `cls.model` instance with the given `filter`"
        if not filter:
            response = db.exec(select(cls.model))
        else:
            response = db.exec(select(cls.model).where(*filter))
        return response

    @classmethod
    def create(cls, data: Optional[dict] = None, db: Optional[Session] = None):
        "Creates an instance of the `cls.model` in the DB given the proper `data`"
        db_model = cls.model(**data)
        db.add(db_model)
        db.commit()
        db.refresh(db_model)
        return db_model

    # TODO actualizar de aca para abajo y agregarlo al service
    @classmethod
    def update(
        cls,
        filter: Optional[list[BinaryExpression]],
        data: Optional[dict[str, Any]] = None,
        db: Session = None,
    ):
        "Updates the `cls.model` filtered by `filter` with the proper `data`"
        db_model = cls.get(filter=filter, db=db).one_or_none()
        if not db_model:
            return None
        for model_attr, attr_value in data.items():
            setattr(db_model, model_attr, attr_value)
        db.add(db_model)
        db.commit()
        db.refresh(db_model)
        return db_model

    @classmethod
    def delete(
        cls, filter: Optional[list[BinaryExpression]], db: Session = None
    ) -> bool:
        """Deletes a `cls.model` instance from the DB given the `id`"""
        db_model = cls.get(filter=filter, db=db).one_or_none()
        if not db_model:
            return False
        db.delete(db_model)
        db.commit()
        return True
