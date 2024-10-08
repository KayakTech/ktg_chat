from sqlalchemy import Column, String, ForeignKey, UUID, Table, JSON
from sqlalchemy.orm import relationship
from app.core.models import BaseModel
from app.database import Base


room_participant = Table(
    "room_participant",
    Base.metadata,
    Column("room_id", UUID(as_uuid=True),
           ForeignKey("rooms.id"), primary_key=True),
    Column("participant_id", UUID(as_uuid=True),
           ForeignKey("participants.id"), primary_key=True),
)


class Room(BaseModel):
    __tablename__ = "rooms"
    name = Column(String)

    organisation_id = Column(
        UUID(as_uuid=True), ForeignKey("organisations.id"))

    chats = relationship("Chat", back_populates="room")
    organisation = relationship("Organisation", back_populates="rooms")

    participants = relationship(
        "Participant", secondary=room_participant, back_populates="rooms")


class Participant(BaseModel):
    __tablename__ = "participants"
    name = Column(String)
    email = Column(String, unique=True, index=True)
    data = Column(JSON)

    rooms = relationship("Room", secondary=room_participant,
                         back_populates="participants")


class Chat(BaseModel):
    __tablename__ = "chats"
    content = Column(String)

    room_id = Column(UUID(as_uuid=True), ForeignKey("rooms.id"))
    created_by_id = Column(UUID(as_uuid=True), ForeignKey("participants.id"))

    room = relationship("Room", back_populates="chats")

    created_by = relationship("Participant")
