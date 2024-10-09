from app.test.base import BaseTest
from fastapi import status
from app.organisation.factories import OrganisationFactory
from app.accounts.factories import UserFactory
from app.chat.factories import RoomFactory, ParticipantFactory, ChatFactory
from uuid import UUID


class TestChat(BaseTest):

    def setup_method(self):
        """Setup method to create an organisation and store its token and ID."""
        self.organisation_info = self.create_organisation()
        self.token = self.organisation_info.get('token')
        self.organisation_id = UUID(self.organisation_info.get('id'))
        self.room = RoomFactory(organisation_id=self.organisation_id)

    def create_organisation(self):
        user = UserFactory()
        self.force_authenticate(user=user)

        organisation = OrganisationFactory(user_id=user.id, is_active=True)

        response = self.client.post(
            f"/organisations/generate-token/{organisation.id}/"
        )

        assert response.status_code == status.HTTP_200_OK

        return response.json()

    def test_get_chat_relelated_data_with_user_token(self):

        user = UserFactory()
        self.force_authenticate(user=user)

        response = self.client.get(
            f"/rooms/{self.room.id}/")

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_get_chat_relelated_data_witout_organisation_token(self):
        user = UserFactory()
        organisation = OrganisationFactory(user_id=user.id, is_active=True)
        self.client.headers = {"Authorization": f"Bearer {organisation.token}"}

        response = self.client.get(
            f"/rooms/{self.room.id}/")

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_get_chat_relelated_data_with_wrong_organisation_token(self):

        response = self.client.get(
            f"/rooms/{self.room.id}/")

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_chat_in_room_not_participant(self):
        self.client.headers = {"Authorization": f"Bearer {self.token}"}

        participant = ParticipantFactory()
        self.db.commit()

        chat_data = {
            "content": "This is a test message",
            "room_id": str(self.room.id),
            "email": participant.email
        }

        response = self.client.post("rooms/chats/", json=chat_data)

        assert response.status_code == status.HTTP_403_FORBIDDEN

        assert response.json() == {
            "detail": "You are not a participant of this room"}

    def test_create_room(self):

        self.client.headers = {"Authorization": f"Bearer {self.token}"}
        data = {
            "name": "Test Room"
        }

        response = self.client.post(
            "/rooms/", json=data
        )

        assert response.status_code == status.HTTP_200_OK

        created_room = response.json()

        assert created_room["name"] == data["name"]

    def test_get_rooms(self):
        self.client.headers = {"Authorization": f"Bearer {self.token}"}

        RoomFactory(organisation_id=self.organisation_id)
        RoomFactory(organisation_id=self.organisation_id)

        response = self.client.get("/rooms/")

        assert response.status_code == status.HTTP_200_OK

        data = response.json()

        assert len(data) == 3

    def test_get_room_by_id(self):

        self.client.headers = {"Authorization": f"Bearer {self.token}"}

        room = RoomFactory(organisation_id=self.organisation_id)

        response = self.client.get(
            f"/rooms/{room.id}/")

        assert response.status_code == status.HTTP_200_OK

        data = response.json()
        assert data["name"] == room.name

    def test_update_room(self):

        self.client.headers = {"Authorization": f"Bearer {self.token}"}

        room = RoomFactory(organisation_id=self.organisation_id)

        updated_data = {
            "name": "Updated Room Name"
        }

        response = self.client.put(f"/rooms/{room.id}/", json=updated_data)
        assert response.status_code == status.HTTP_200_OK

        updated_room = response.json()
        assert updated_room["name"] == updated_data["name"]

    def test_delete_room(self):
        self.client.headers = {"Authorization": f"Bearer {self.token}"}

        room = RoomFactory(organisation_id=self.organisation_id)

        response = self.client.delete(f"/rooms/{room.id}/")
        assert response.status_code == status.HTTP_200_OK

        # Verify the room has been deleted
        response = self.client.get(f"/rooms/{room.id}/")
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_add_participant_to_room(self):

        self.client.headers = {"Authorization": f"Bearer {self.token}"}

        participant = ParticipantFactory()

        response = self.client.post(
            f"/rooms/{self.room.id}/add-participant/",
            json={"name": participant.name, "email": participant.email}
        )
        assert response.status_code == status.HTTP_200_OK
        assert response.json()["message"] == "Participant added successfully"

    def test_get_participants_in_room(self):
        self.client.headers = {"Authorization": f"Bearer {self.token}"}

        participant = ParticipantFactory()

        self.room.participants.append(participant)
        self.db.commit()

        response = self.client.get(f"/rooms/{self.room.id}/participants/")

        assert response.status_code == status.HTTP_200_OK

        participants = response.json()

        assert len(participants) > 0

        assert any(p['email'] == participant.email for p in participants)

    def test_create_chat(self):
        self.client.headers = {"Authorization": f"Bearer {self.token}"}

        participant = ParticipantFactory()

        # Add participant to room
        self.client.post(
            f"/rooms/{self.room.id}/add-participant/",
            json={"name": participant.name, "email": participant.email}
        )

        data = {
            "content": "Hello World",
            "room_id": str(self.room.id),
            "email": participant.email
        }

        response = self.client.post("rooms/chats/", json=data)

        assert response.status_code == status.HTTP_200_OK

        created_chat = response.json()
        assert created_chat["content"] == data["content"]

    def test_get_my_room(self):
        self.client.headers = {"Authorization": f"Bearer {self.token}"}

        participant = ParticipantFactory()

        self.room.participants.append(participant)
        self.db.commit()

        response = self.client.get(
            f"/rooms/my-rooms/{participant.email}/")

        assert response.status_code == status.HTTP_200_OK

        for room in response.json():
            if room['id'] == str(self.room.id):
                participants_in_room = room.get('participants', [])

                print(participants_in_room)
                assert any(
                    p['email'] == participant.email for p in participants_in_room)
                break

    def test_get_chats_in_room(self):
        self.client.headers = {"Authorization": f"Bearer {self.token}"}

        participant = ParticipantFactory()

        # Add participant to room
        self.client.post(
            f"/rooms/{self.room.id}/add-participant/",
            json={"name": participant.name, "email": participant.email}
        )

        chat = ChatFactory(room_id=self.room.id, created_by_id=participant.id)

        response = self.client.get(f"rooms/chats/{self.room.id}/")
        assert response.status_code == status.HTTP_200_OK

        chats = response.json()
        assert len(chats) > 0
        assert chats[0]["content"] == chat.content
