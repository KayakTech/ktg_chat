from pydantic import BaseModel, Field
from datetime import datetime

from app.accounts.schemas import UserResponseSchema, UserSchema
from typing import Optional
from uuid import UUID


class CreateTodoSchema(BaseModel):
    title: str
    description: str

    class Config:
        from_attributes = True


class TodoResponseSchema(BaseModel):
    id: Optional[UUID] = Field(None)
    title: str
    description: str
    user_id: UUID
    created_at: datetime = Field(
        default_factory=datetime.now)
    updated_at: datetime = Field(
        default_factory=datetime.now)
    created_by: UserResponseSchema

    class Config:
        from_attributes = True
