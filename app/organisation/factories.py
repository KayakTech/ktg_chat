import factory
import factory.random
from .models import Organisation
from app.test.base import BaseTest
from accounts.factories import UserFactory


class OrganisationFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = Organisation
        sqlalchemy_session = BaseTest.get_db()
        sqlalchemy_session_persistence = 'commit'

    name = factory.Faker('name')
    description = factory.Faker('text')
    user_id = factory.SubFactory(UserFactory)
