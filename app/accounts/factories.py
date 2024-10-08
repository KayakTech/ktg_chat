import factory
from .models import User
from app.test.base import BaseTest


class UserFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = User
        sqlalchemy_session = BaseTest.get_db()
        sqlalchemy_session_persistence = 'commit'

    is_active = True
    email = factory.Faker('email')
