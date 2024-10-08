
from sqlalchemy.orm import Session
from .models import Room, Participant
from sqlalchemy import UUID
from typing import List


def get_rooms_for_participant(session: Session,  participant_email: str) -> List[Room]:
    return (
        session.query(Room)
        .join(Room.participants)
        .filter(Participant.email == participant_email)
        .all()
    )


def add_participant_to_room(session: Session, room_id: UUID, participant_data: dict):
    room = session.query(Room).filter(Room.id == room_id).one_or_none()

    if not room:
        raise ValueError("Room not found")

    participant = session.query(Participant).filter(
        Participant.email == participant_data['email']).one_or_none()

    if not participant:
        participant = Participant(
            name=participant_data['name'],
            email=participant_data['email'],
            data=participant_data.get('data', None)
        )
        session.add(participant)

    if participant not in room.participants:
        room.participants.append(participant)

    session.commit()
    session.refresh(room)


def get_participants_in_room(session: Session, room_id: UUID):
    room = session.query(Room).filter(Room.id == room_id).one_or_none()

    if room is None:
        raise ValueError("Room not found")

    return room.participants


def remove_participant_from_room(session: Session, room_id: UUID, participant_email: str):

    room = session.query(Room).filter(Room.id == room_id).one_or_none()

    if room is None:
        raise ValueError("Room not found")

    participant = session.query(Participant).filter(
        Participant.email == participant_email).one_or_none()

    if participant is None:
        raise ValueError("Participant not found")

    if participant in room.participants:
        room.participants.remove(participant)

    session.commit()
