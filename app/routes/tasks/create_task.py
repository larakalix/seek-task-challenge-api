from fastapi import APIRouter, Depends, HTTPException, Request
from app.models.task_model import Task, TaskCreate
from app.dependencies import get_task_command_handler
from app.auth_helpers import get_session_from_request, TokenData
from app.database import db

router = APIRouter()

@router.post("/tasks", response_model=Task)
async def create_task(
    request: Request,
    task_create: TaskCreate,
    command_handler = Depends(get_task_command_handler)
):
    session = await get_session_from_request(request)
    user_email = session.get("user_email")
    user_doc = await db.users.find_one({"email": user_email})
    
    if not user_doc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found"
        )
        
    user_id = str(user_doc["_id"])
    user_name = user_doc["name"]
    created_task = await command_handler.create_task(task_create, user_id, user_name)
    return created_task