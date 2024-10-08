import factory
import factory.random
from .models import Todo
from app.test.base import BaseTest
from app.accounts.factories import UserFactory

class TodoFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = Todo
        sqlalchemy_session =  BaseTest.get_db()
        sqlalchemy_session_persistence = 'commit'

    title = factory.Faker('name')
    description = factory.Faker('text')
    created_by = factory.SubFactory(UserFactory)
  
