

from pydantic import BaseModel
from typing import Optional
from uuid import UUID
from pydantic import Field


class BaseUserSchema(BaseModel):
    id: Optional[UUID] = Field(None)
    username: str | None = None
    email: str
    full_name: str | None = None
    is_active: bool | None = None

    class Config:
        from_attributes = True


class UserSchema(BaseUserSchema):
    password: str | None = None


class UserResponseSchema(BaseUserSchema):
    pass
