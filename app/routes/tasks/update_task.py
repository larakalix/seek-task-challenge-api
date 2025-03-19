from fastapi import APIRouter, Depends, HTTPException, Request
from app.models.task_model import Task, TaskUpdate
from app.dependencies import get_task_command_handler
from app.auth_helpers import get_session_from_request

router = APIRouter()

@router.put("/tasks/{task_id}", response_model=Task)
async def update_task(
    request: Request,
    task_id: str, 
    task_update: TaskUpdate,
    command_handler = Depends(get_task_command_handler)
):
    session = await get_session_from_request(request)
    
    updated_task = await command_handler.update_task(task_id, task_update, session.get("user_id"))
    return updated_task