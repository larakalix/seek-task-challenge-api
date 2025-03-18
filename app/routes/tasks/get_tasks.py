from fastapi import APIRouter, Depends
from typing import List
from app.models.task_model import Task
from app.repositories.task_repository import TaskRepository
from app.dependencies import get_task_repository

router = APIRouter()

@router.get("/tasks", response_model=List[Task])
async def get_tasks(repo: TaskRepository = Depends(get_task_repository)):
    tasks_list = await repo.get_tasks()
    return [Task(**task) for task in tasks_list]
