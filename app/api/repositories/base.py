from typing import Any, Optional
from fastapi import HTTPException, logger, status
from sqlalchemy.exc import IntegrityError

from sqlmodel import Session, select


class BaseRepository:
    model = None

    @classmethod
    def get_one(
        cls, filter: Optional[dict] = None, db: Optional[Session] = None
    ) -> model:
        try:
            sql_filter = [getattr(cls.model, k) == v for k, v in filter.items()]
            response = db.exec(select(cls.model).where(*sql_filter)).first()
            if not response:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"{cls.model.__name__} Not found",
                )
            return response
        except AttributeError as e:
            logger.logger.error(e)
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid filter parameter",
            )
        except Exception as e:
            logger.logger.error(e)
            raise HTTPException(
                status_code=status.HTTP_418_IM_A_TEAPOT, detail="Unhandled Error"
            )

    @classmethod
    def get_all(cls, db: Optional[Session] = None):
        try:
            response = db.exec(select(cls.model)).all()
            if not response:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"{cls.model.__name__} Not found",
                )
            return response

        except Exception as e:
            logger.logger.error(e)
            raise HTTPException(
                status_code=status.HTTP_418_IM_A_TEAPOT, detail="Unhandled Error"
            )

    @classmethod
    def create(cls, data: Optional[dict] = None, db: Optional[Session] = None):
        try:
            db_model = cls.model(**data)
            db.add(db_model)
            db.commit()
            db.refresh(db_model)
            return db_model
        except IntegrityError as e:
            print(e)
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"{cls.model.__name__} already exists",
            )
        except Exception as e:
            print(e)
            raise HTTPException(
                status_code=status.HTTP_418_IM_A_TEAPOT, detail="Unhandled Error"
            )

    @classmethod
    def patch(cls, id: int, data: Optional[dict[str, Any]] = None, db: Session = None):
        db_model = cls.get_one(filter={"id": id}, db=db)
        for model_attr, attr_value in data.items():
            setattr(db_model, model_attr, attr_value)
        db.add(db_model)
        db.commit()
        db.refresh(db_model)
        return db_model

    @classmethod
    def delete(cls, id: int, db: Session = None):
        try:
            db_model = cls.get_one(filter={"id": id}, db=db)
            db.delete(db_model)
            db.commit()
            return None
        except Exception as e:
            logger.logger.exception(e)
            raise HTTPException(
                status_code=status.HTTP_418_IM_A_TEAPOT, detail="Unhandled Error"
            )
