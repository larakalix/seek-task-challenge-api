from fastapi import APIRouter, Depends
from app.models.task_model import Task
from app.dependencies import get_task_command_handler
from app.auth import verify_token

router = APIRouter(dependencies=[Depends(verify_token)])

@router.delete("/tasks/{task_id}", response_model=Task)
async def delete_task(
    task_id: str,
    command_handler = Depends(get_task_command_handler)
):
    deleted_task = await command_handler.delete_task(task_id)
    return deleted_task