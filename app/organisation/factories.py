import factory
import factory.random
from app.organisation.models import Organisation
from app.test.base import BaseTest
from uuid import uuid4
import string
import random


class OrganisationFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = Organisation
        sqlalchemy_session = BaseTest.get_db()
        sqlalchemy_session_persistence = 'commit'

    name = factory.Faker('name')
    email = factory.Faker('email')
    description = factory.Faker('text')
    user_id = factory.LazyFunction(uuid4)
    token = factory.LazyFunction(lambda: ''.join(
        random.choices(string.ascii_letters + string.digits, k=32)))

    is_active = factory.Faker('boolean')
