

from sqlalchemy import Column, Integer, DateTime
from sqlalchemy.sql import func
from app.database import Base
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
import uuid


class BaseModel(Base):
    __abstract__ = True

    id = Column(PG_UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True),
                        server_default=func.now(), onupdate=func.now())
