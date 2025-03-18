from fastapi import APIRouter, Depends
from app.models.task_model import Task, TaskUpdate
from app.dependencies import get_task_command_handler
from app.auth_helpers import verify_token

router = APIRouter(dependencies=[Depends(verify_token)])

@router.put("/tasks/{task_id}", response_model=Task)
async def update_task(
    task_id: str, 
    task_update: TaskUpdate,
    command_handler = Depends(get_task_command_handler)
):
    updated_task = await command_handler.update_task(task_id, task_update)
    return updated_task