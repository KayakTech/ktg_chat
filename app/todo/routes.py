from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.accounts.schemas import UserSchema
from app.authentication.utils import get_current_active_user
from fastapi_utils.cbv import cbv
from app.dependencies import get_db
from .schemas import CreateTodoSchema, TodoResponseSchema
from .models import Todo
from . import services

router = APIRouter(

)

# @router.post("/")
# async def create_todo(self, todo: CreateTodoSchema,current_user = Depends(get_current_active_user) ):
#     return [{"todo": "todo"}]


@cbv(router)  # Step 2: Create and decorate a class to hold the endpoints
class TodoView:
    # Step 3: Add dependencies as class attributes
    current_user: UserSchema = Depends(get_current_active_user)
    db: Session = Depends(get_db)

    @router.get("/{id}", response_model=TodoResponseSchema)
    async def get_todos(self, id: int):
        todo = services.get_todo_by_id(self.db, id)
        return todo

    @router.get("/", response_model=list[TodoResponseSchema])
    async def get_todo(self):
        todos = services.get_todos(self.db, self.current_user.id)
        return todos

    @router.post("/", response_model=TodoResponseSchema)
    async def create_todo(self, data: CreateTodoSchema):
        todo = Todo(user_id=self.current_user.id, **data.__dict__)
        todo = services.create_todo(self.db, todo)
        return todo
