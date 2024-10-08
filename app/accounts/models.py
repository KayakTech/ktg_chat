
from sqlalchemy import Boolean, Column, String
from sqlalchemy.orm import relationship
from app.core.models import BaseModel
# from app.chat.models import room_participant


class User(BaseModel):
    __tablename__ = "users"
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)

    todos = relationship("Todo", back_populates="created_by")

    organisations = relationship("Organisation", back_populates='user')

    # rooms = relationship("Room", secondary='room_participant',
    #                      back_populates="participants")
