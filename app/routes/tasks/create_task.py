from fastapi import APIRouter, Depends
from app.models.task_model import Task, TaskCreate
from app.dependencies import get_task_command_handler
from app.auth import verify_token
from app.database import db

router = APIRouter(dependencies=[Depends(verify_token)])

@router.post("/tasks", response_model=Task)
async def create_task(
    task_create: TaskCreate,
    command_handler = Depends(get_task_command_handler)
):
    created_task = await command_handler.create_task(task_create)
    return created_task