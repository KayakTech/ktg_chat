import factory
import factory.random
from .models import Chat, Room, Participant
from app.test.base import BaseTest
from uuid import uuid4
from faker import Faker
import random

fake = Faker()


class RoomFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = Room
        sqlalchemy_session = BaseTest.get_db()
        sqlalchemy_session_persistence = 'commit'

    name = factory.Faker('name')
    organisation_id = factory.LazyFunction(uuid4)
    created_at = factory.Faker('date_time')
    updated_at = factory.Faker('date_time')


class ParticipantFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = Participant
        sqlalchemy_session = BaseTest.get_db()
        sqlalchemy_session_persistence = 'commit'

    name = factory.Faker('name')
    email = email = factory.Faker('email')
    created_at = factory.Faker('date_time')
    updated_at = factory.Faker('date_time')
    data = factory.LazyFunction(lambda: {
        "key1": fake.word(),
        "key2": random.randint(1, 100),
        "key3": [fake.name() for _ in range(3)]
    })


class ChatFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = Chat
        sqlalchemy_session = BaseTest.get_db()
        sqlalchemy_session_persistence = 'commit'

    content = factory.Faker('name')
    room_id = factory.SubFactory(RoomFactory)
    created_by_id = factory.LazyFunction(uuid4)
    created_at = factory.Faker('date_time')
    updated_at = factory.Faker('date_time')
