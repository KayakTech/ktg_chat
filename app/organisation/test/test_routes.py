from app.test.base import BaseTest
from fastapi import status
from app.organisation.factories import OrganisationFactory
from app.accounts.factories import UserFactory


class TestOrganisation(BaseTest):

    def test_create_organisation(self):
        self.force_authenticate(user=None)
        data = {
            "name": "Test Organisation",
            "email": "test@organisation.com",
            "description": "Test description",
            "is_active": True,
        }

        response = self.client.post("/organisations/", json=data)
        # Check for forbidden without auth
        assert response.status_code == status.HTTP_403_FORBIDDEN

        user = UserFactory()
        self.force_authenticate(user=user)

        response = self.client.post("/organisations/", json=data)
        assert response.status_code == status.HTTP_200_OK

        created_organisation = response.json()
        assert created_organisation["email"] == data["email"]
        #
        assert created_organisation["name"] == data["name"]

    def test_get_organisation(self):
        user = UserFactory()
        self.force_authenticate(user=user)

        organisation = OrganisationFactory(user_id=user.id)
        response = self.client.get(f"/organisations/{organisation.id}")
        assert response.status_code == status.HTTP_200_OK

        data = response.json()
        assert data["email"] == organisation.email
        assert data["name"] == organisation.name

    def test_get_all_organisations(self):
        user = UserFactory()
        self.force_authenticate(user=user)

        OrganisationFactory.create_batch(2, user_id=user.id)

        response = self.client.get("/organisations/")
        assert response.status_code == status.HTTP_200_OK

        data = response.json()
        assert len(data) == 2

    def test_update_organisation(self):
        user = UserFactory()
        self.force_authenticate(user=user)

        organisation = OrganisationFactory(user_id=user.id)

        updated_data = {
            "name": "Updated Organisation",
            "email": "updated@organisation.com",
            "description": "Updated description",
        }

        response = self.client.put(
            f"/organisations/{organisation.id}", json=updated_data)
        assert response.status_code == status.HTTP_200_OK

        updated_organisation = response.json()
        assert updated_organisation["name"] == updated_data["name"]
        assert updated_organisation["email"] == updated_data["email"]

    def test_delete_organisation(self):
        user = UserFactory()
        self.force_authenticate(user=user)

        organisation = OrganisationFactory(user_id=user.id)

        response = self.client.delete(f"/organisations/{organisation.id}")
        assert response.status_code == status.HTTP_200_OK

        # Verify the organisation has been deleted
        response = self.client.get(f"/organisations/{organisation.id}")
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_generate_token(self):
        user = UserFactory()
        self.force_authenticate(user=user)

        organisation = OrganisationFactory(user_id=user.id)

        response = self.client.post(
            f"/organisations/generate-token/{organisation.id}")
        assert response.status_code == status.HTTP_200_OK

        updated_organisation = response.json()
        assert "token" in updated_organisation
        assert updated_organisation["token"] is not None
