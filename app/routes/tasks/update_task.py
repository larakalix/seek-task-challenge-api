from fastapi import APIRouter, Depends
from app.auth import verify_token
from app.models import Task, TaskUpdate
from app.repositories.task_repository import TaskRepository
from app.dependencies import get_task_repository

router = APIRouter(dependencies=[Depends(verify_token)])

@router.put("/tasks/{task_id}", response_model=Task)
async def update_task(task_id: str, task_update: TaskUpdate, repo: TaskRepository = Depends(get_task_repository)):
    updated_task = await repo.update_task(task_id, task_update)
    return Task(**updated_task)
