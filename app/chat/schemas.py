from pydantic import BaseModel, Field, EmailStr
from typing import Optional, Dict, Any, List

from uuid import UUID
from app.core.schema import BaseSchema


class RoomSchema(BaseSchema, BaseModel):
    name: str

    class Config:
        from_attributes = True


class RoomSchemaResponse(BaseSchema, BaseModel):
    name: str
    organisation_id: Optional[UUID]
    organisation_id: Optional[UUID]
    participants: List['ParticipantSchema']

    class Config:
        from_attributes = True


class ChatSchema(BaseSchema, BaseModel):
    content: str
    room_id: Optional[UUID]
    email: Optional[EmailStr] = Field(None)

    class Config:
        from_attributes = True


class ChatResponseSchema(BaseSchema, BaseModel):
    content: str
    room_id: Optional[UUID]
    created_by: Optional['ParticipantSchema']

    class Config:
        from_attributes = True


class ParticipantSchema(BaseSchema, BaseModel):
    name: str
    email: EmailStr
    data: Optional[Dict[str, Any]] = Field(None)

    class Config:
        from_attributes = True
