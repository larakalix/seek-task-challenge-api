from fastapi import APIRouter, Depends, HTTPException
from app.models.task_model import Task, TaskCreate
from app.repositories.task_repository import TaskRepository
from app.dependencies import get_task_repository
from app.auth import verify_token
from app.database import db

router = APIRouter(dependencies=[Depends(verify_token)])

@router.post("/tasks", response_model=Task)
async def create_task(
    task_create: TaskCreate,
    repo: TaskRepository = Depends(get_task_repository),
    token_payload: dict = Depends(verify_token)
):
    user_email = token_payload.get("email")
    if not user_email:
        raise HTTPException(status_code=401, detail="Invalid token payload")
    user_doc = await db.users.find_one({"email": user_email})
    if not user_doc:
        raise HTTPException(status_code=401, detail="User not found")
    user_id = str(user_doc["_id"])
    user_name = user_doc["name"]
    created_task = await repo.create_task(task_create, user_id, user_name)
    return Task(**created_task)