
from sqlalchemy import Boolean, Column, String
from sqlalchemy.orm import relationship
from app.core.models import BaseModel


class User(BaseModel):
    __tablename__ = "users"
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)

    organisations = relationship("Organisation", back_populates='user')
