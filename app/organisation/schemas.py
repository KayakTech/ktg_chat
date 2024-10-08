from pydantic import BaseModel, Field, EmailStr
from typing import Optional
from uuid import UUID
from app.accounts.schemas import UserResponseSchema
from app.core.schema import BaseSchema


class OrganisationSchema(BaseSchema, BaseModel):
    name: str
    email: EmailStr
    description: Optional[str] = None
    user_id: Optional[UUID] = Field(None)
    is_active: Optional[bool] = Field(None)

    class Config:
        # orm_mode = True
        from_attributes = True


class OrganisationResponseSchema(BaseSchema, BaseModel):
    name: str
    email:   Optional[EmailStr] = Field(None)
    description: Optional[str] = None
    token: Optional[str] = Field(None)
    user: Optional[UserResponseSchema] = None
    is_active:  Optional[bool] = None

    class Config:
        # orm_mode = True
        from_attributes = True
