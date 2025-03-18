from fastapi import APIRouter
from uuid import uuid4
from app.models import Task, TaskCreate, TaskStatus
from app.database import db

router = APIRouter()

@router.post("/tasks", response_model=Task)
async def create_task(task_create: TaskCreate):
    new_task = {
        "title": task_create.title,
        "description": task_create.description,
        "status": TaskStatus.Todo,
    }
    result = await db.tasks.insert_one(new_task)
    created_task = await db.tasks.find_one({"_id": result.inserted_id})
    created_task["id"] = str(created_task["_id"])
    return Task(**created_task)