
from app.test.base import BaseTest
from fastapi import status

from app.organisation.factories import OrganisationFactory
from .. import services
from app.accounts.factories import UserFactory
from app.todo.models import Todo


class OrganisationTest(BaseTest):
    def test_create_todo(self):
        self.force_authenticate(user=None)
        data = {
            "title": "Test",
            "description": "Test",
            "user_id": UserFactory().id,

        }

        response = self.client.post("/organisation/", json=data)
        assert response.status_code == status.HTTP_403_FORBIDDEN

        user = UserFactory()
        self.force_authenticate(user=user)

        response = self.client.post("/organisation/", json=data)
        assert response.status_code == status.HTTP_200_OK

        # user_todo = services.get_user_project(self.db, user.id)
        # assert user_todo.count() == 1

    # def test_get_todo(self):
    #     user = UserFactory()
    #     self.force_authenticate(user=user)

    #     all_todos = self.db.query(Todo)
    #     user_todos = services.get_user_project(self.db, user.id)

    #     assert user_todos.count() == 1
    #     assert all_todos.count() >= 2

    #     response = self.client.get(f"/organisation/")
    #     assert response.status_code == status.HTTP_200_OK

    #     data = response.json()
    #     assert len(data) == 1

    # def test_get_todo_by_id(self):
    #     user = UserFactory()
    #     self.force_authenticate(user=user)

    #     todo = OrganisationFactory(created_by=user)
    #     response = self.client.get(f"/organisation/{todo.id}")
    #     assert response.status_code == status.HTTP_200_OK

    #     data = response.json()
    #     assert data["title"] == todo.title
    #     # assert data["description"] == todo.description
    #     # assert data["user_id"] == user.id
    #     # assert data['created_by']['email'] == user.email
