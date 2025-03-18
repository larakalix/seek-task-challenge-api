from fastapi import APIRouter, Depends
from app.auth import verify_token
from app.models import Task
from app.repositories.task_repository import TaskRepository
from app.dependencies import get_task_repository

router = APIRouter(dependencies=[Depends(verify_token)])

@router.delete("/tasks/{task_id}", response_model=Task)
async def soft_delete_task(task_id: str, repo: TaskRepository = Depends(get_task_repository)):
    deleted_task = await repo.soft_delete_task(task_id)
    return Task(**deleted_task)
