
from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional
from uuid import UUID


class BaseSchema(BaseModel):
    id: Optional[UUID] = Field(None)
    created_at: Optional[datetime] = Field(
        default_factory=datetime.utcnow)
    updated_at: Optional[datetime] = Field(
        default_factory=datetime.utcnow)

    class Config:
        # orm_mode = True
        from_attributes = True
