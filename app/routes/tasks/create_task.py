from fastapi import APIRouter, Depends, HTTPException
from app.models.task_model import Task, TaskCreate
from app.dependencies import get_task_command_handler
from app.auth import verify_token
from app.database import db

router = APIRouter(dependencies=[Depends(verify_token)])

@router.post("/tasks", response_model=Task)
async def create_task(
    task_create: TaskCreate,
    token_payload: dict = Depends(verify_token),
    command_handler = Depends(get_task_command_handler)
):
    user_email = token_payload.get("email")
    if not user_email:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token payload"
        )
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