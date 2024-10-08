
from sqlalchemy.orm import Session
from .models import Todo


def get_todos(db: Session, user_id: int):
    return db.query(Todo).filter(Todo.user_id == user_id)


def get_todo_by_id(db: Session, todo_id: int):
    return db.query(Todo).filter(Todo.id == todo_id).first()


def create_todo(db: Session, todo: Todo):
    db.add(todo)
    db.commit()
    db.refresh(todo)
    return todo
