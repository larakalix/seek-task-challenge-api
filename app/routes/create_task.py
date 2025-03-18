from fastapi import APIRouter
from uuid import uuid4
from app.models import Task, TaskCreate, TaskStatus
from app.data import tasks

router = APIRouter()

@router.post("/tasks", response_model=Task)
def create_task(task_create: TaskCreate):
    task_id = str(uuid4())
    new_task = Task(
        id=task_id,
        title=task_create.title,
        description=task_create.description,
        status=TaskStatus.Todo,
    )
    tasks.append(new_task)
    return new_task