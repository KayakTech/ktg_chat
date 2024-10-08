from sqlalchemy import Column, ForeignKey, String, UUID, Boolean

from sqlalchemy.orm import relationship
from app.core.models import BaseModel


class Organisation(BaseModel):
    __tablename__ = "organisations"
    name = Column(String, index=True)
    email = Column(String, unique=True)
    description = Column(String)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    token = Column(String, unique=True)
    is_active = Column(Boolean, default=True)

    user = relationship("User", back_populates='organisations')
    rooms = relationship('Room', back_populates='organisation')
