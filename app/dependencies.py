from app.repositories.task_repository import TaskRepository
from app.database import db

def get_task_repository() -> TaskRepository:
    return TaskRepository(db)
