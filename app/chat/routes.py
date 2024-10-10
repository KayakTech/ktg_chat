from fastapi import APIRouter, Depends, Request, HTTPException, status
from sqlalchemy.orm import Session
from app.accounts.schemas import UserSchema
from app.authentication.utils import get_current_active_organisation
from fastapi_utils.cbv import cbv
from app.dependencies import get_db
from pydantic import UUID4
from app.core.dependency_injection import service_locator
from app.chat.models import Room
from app.chat.schemas import RoomSchema, ChatSchema, ParticipantSchema, RoomSchemaResponse, ChatResponseSchema
from typing import List
from app.chat import services
from app.chat.models import Chat, Participant

router = APIRouter(

)


@cbv(router)
class RoomView:
    current_organisation: UserSchema = Depends(get_current_active_organisation)
    db: Session = Depends(get_db)

    @router.get("/", response_model=list[RoomSchemaResponse])
    @router.post("/", response_model=RoomSchema)
    async def rooms(self, request: Request, data: RoomSchema = None):

        if request.method == "GET":

            filter_values = {
                'organisation_id': self.current_organisation.id
            }

            return service_locator.general_service.filter_data(self.db, filter_values, Room)

        data.__dict__['organisation_id'] = self.current_organisation.id

        data = Room(**data.__dict__)

        response = service_locator.general_service.create_data(self.db, data)
        return response

    @router.get("/my-rooms/{email}/", response_model=list[RoomSchemaResponse])
    def get_user_rooms(self, email: str):
        rooms = services.get_rooms_for_participant(self.db, email)

        if not rooms:
            raise HTTPException(
                status_code=404, detail="No rooms found for this user.")

        return rooms

    @router.get("/{id}/", response_model=RoomSchemaResponse)
    async def get_room(self, id: UUID4):

        response = service_locator.general_service.get_data_by_id(
            self.db, id, Room)
        return response

    @router.delete("/{id}/")
    async def delete_room(self, id: UUID4):
        response = service_locator.general_service.delete_data(
            self.db, id, Room)

        return response

    @router.put("/{id}/", response_model=RoomSchema)
    @router.patch("/{id}", response_model=RoomSchema)
    async def update_room(self, id: UUID4, data: RoomSchema):
        data = data.dict(exclude_unset=True)

        response = service_locator.general_service.update_data(
            self.db, key=id, data=data, model=Room)

        return response

    @router.post("/chats/", response_model=ChatResponseSchema)
    async def create_chat(self, request: Request, data: ChatSchema):
        email = data.email

        if not email:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email is required"
            )

        # Fetch participant by email
        participant = service_locator.general_service.get_participant_data(
            self.db, {"email": email}, Participant, single_record=True
        )

        if not participant:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Participant not found"
            )

        # Fetch the room and check if participant is part of it
        room = self.db.query(Room).filter(
            Room.id == data.room_id).one_or_none()

        if not room or participant not in room.participants:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You are not a participant of this room"
            )

        chat = Chat(**data.dict(exclude={'email'}),
                    created_by_id=participant.id)

        chats = service_locator.general_service.create_data(self.db, chat)
        return chats

    @router.get("/chats/{room_id}/", response_model=list[ChatResponseSchema])
    async def get_chats_in_room(self, room_id: UUID4):
        service_locator.general_service.raise_not_found(Chat)

        chats = self.db.query(Chat).filter(Chat.room_id == room_id).all()

        return chats

    @router.put("/chats/{id}/", response_model=ChatResponseSchema)
    @router.patch("/chats/{id}/", response_model=ChatResponseSchema)
    async def update_chat(self, id: UUID4, data: ChatSchema):
        data = data.dict(exclude_unset=True)

        response = service_locator.general_service.update_data(
            self.db, key=id, data=data, model=Chat)

        return response

    @router.post("/{room_id}/add-participant/", response_model={})
    async def add_participant(self, room_id: UUID4, data: ParticipantSchema):

        try:

            services.add_participant_to_room(self.db, room_id, data.dict())
            return {"message": "Participant added successfully"}
        except ValueError as e:
            raise HTTPException(status_code=404, detail=str(e))

    @router.get("/{room_id}/participants/", response_model=List[ParticipantSchema])
    async def get_participants(self, room_id: UUID4):

        try:
            participants = services.get_participants_in_room(self.db, room_id)

            return participants
        except ValueError as e:

            raise HTTPException(status_code=404, detail=str(e))

    @router.post("/{room_id}/remove-participant/{participant_email}")
    def delete_participant(self, room_id: UUID4, participant_email: str, session: Session = Depends(get_db)):
        try:

            services.remove_participant_from_room(
                self.db, room_id, participant_email)
            return {"message": "Participant removed from the room."}
        except ValueError as e:
            raise HTTPException(status_code=404, detail=str(e))
