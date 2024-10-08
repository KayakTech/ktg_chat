import factory
import factory.random
from .models import Chat
from app.test.base import BaseTest


class ChatFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = Chat
        sqlalchemy_session = BaseTest.get_db()
        sqlalchemy_session_persistence = 'commit'

    name = factory.Faker('name')
    description = factory.Faker('text')
