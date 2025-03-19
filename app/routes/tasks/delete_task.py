from fastapi import APIRouter, Depends, Request
from app.models.task_model import Task
from app.dependencies import get_task_command_handler
from app.auth_helpers import get_session_from_request

router = APIRouter()

@router.delete("/tasks/{task_id}", response_model=Task)
async def delete_task(
    request: Request,
    task_id: str,
    command_handler = Depends(get_task_command_handler)
):
    session = await get_session_from_request(request)
    
    deleted_task = await command_handler.delete_task(task_id, session.get("user_id"))
    return deleted_task