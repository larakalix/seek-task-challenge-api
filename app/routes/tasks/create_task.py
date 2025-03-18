from fastapi import APIRouter, Depends
from app.auth import verify_token
from app.models import Task, TaskCreate
from app.repositories.task_repository import TaskRepository
from app.dependencies import get_task_repository

router = APIRouter(dependencies=[Depends(verify_token)])

@router.post("/tasks", response_model=Task)
async def create_task(task_create: TaskCreate, repo: TaskRepository = Depends(get_task_repository)):
    created_task = await repo.create_task(task_create)
    return Task(**created_task)
