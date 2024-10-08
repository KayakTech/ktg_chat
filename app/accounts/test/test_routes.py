
from app.test.base import BaseTest
from fastapi import status
from ..factories import UserFactory


class TestAccount(BaseTest):
    def test_get_user(self):

        user = UserFactory()

        self.force_authenticate(user)
        response = self.client.get("/accounts/me/")

        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["email"] == user.email
