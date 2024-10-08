
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, UUID
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.core.models import BaseModel

import typing

if typing.TYPE_CHECKING:
    from app.accounts.models import User


class Todo(BaseModel):
    __tablename__ = "todo"

    title = Column(String, index=True)
    description = Column(String, index=True)
    user_id = Column(UUID, ForeignKey("users.id"))
    created_by = relationship("User", back_populates="todos")

    def __repr__(self):
        return f"<Todo {self.title}> - {self.user_id}"

    def __str__(self):
        return f"<Todo {self.title}> - {self.user_id}"
