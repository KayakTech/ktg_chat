
from sqlalchemy import Column, String, ForeignKey, UUID
from app.core.models import BaseModel


class Todo(BaseModel):
    __tablename__ = "todo"

    title = Column(String, index=True)
    description = Column(String, index=True)
    user_id = Column(UUID, ForeignKey("users.id"))

    def __repr__(self):
        return f"<Todo {self.title}> - {self.user_id}"

    def __str__(self):
        return f"<Todo {self.title}> - {self.user_id}"
