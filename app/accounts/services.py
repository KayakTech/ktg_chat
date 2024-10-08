
from sqlalchemy.orm import Session
import typing
from . import models

if typing.TYPE_CHECKING:
    from app.authentication.schemas import UserRegistrationForm


def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()


def create_user(db: Session, user: "UserRegistrationForm"):
    from app.authentication.utils import get_password_hash
    hashed_password = get_password_hash(user.password)
    # if user already exists, return None
    if db.query(models.User).filter(models.User.email == user.email).first():
        raise ValueError("User already exists")

    db_user = models.User(email=user.email, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
