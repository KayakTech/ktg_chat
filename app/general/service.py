from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from pydantic import BaseModel
from pydantic import UUID4
from app.chat.models import Participant


class GeneralService:

    def create_data(self, db: Session, model):
        db.add(model)
        db.commit()
        db.refresh(model)
        return model

    def list_data(self, db: Session, model: BaseModel):
        return db.query(model).all()

    def get_data_by_id(self, db: Session, project_id: UUID4, model: BaseModel):
        project = db.query(model).filter(
            model.id == project_id).first()
        self.raise_not_found(project)
        return project

    def delete_data(self, db: Session, project_id: UUID4, model: BaseModel):
        project = db.query(model).filter(
            model.id == project_id).first()
        self.raise_not_found(project)
        db.delete(project)
        db.commit()
        return {"detail": "Organisation deleted successfully"}

    def update_data(self, db: Session, key: UUID4, data: dict, model: BaseModel):
        project = db.query(model).filter(
            model.id == key).first()
        self.raise_not_found(project)

        for key, value in data.items():
            if hasattr(project, key):
                setattr(project, key, value)

        db.commit()
        db.refresh(project)
        return project

    def filter_data(self, db: Session, filter_values: dict, model: BaseModel, single: bool = False):
        query = db.query(model)

        for key, value in filter_values.items():
            if hasattr(model, key):
                query = query.filter(getattr(model, key) == value)

        return query.one_or_none() if single else query.all()

    def get_participant_by_email(self, db: Session, email: str, model: BaseModel) -> Participant:
        participant = self.filter_data(db, {"email": email}, model, True)

        if participant is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail={"error": "Participant not found with this email"}
            )

        return participant

    def raise_not_found(self, model: BaseModel):
        if model is None:

            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,

                detail=f"{status.HTTP_404_NOT_FOUND} Not Found"
            )
        return object
