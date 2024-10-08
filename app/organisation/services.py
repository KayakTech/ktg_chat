

from sqlalchemy.orm import Session
from .models import Organisation
from uuid import UUID


def get_user_project(db: Session, user_id: UUID):
    return db.query(Organisation).filter(Organisation.user_id == user_id)
