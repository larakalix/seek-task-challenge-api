from fastapi import APIRouter
from typing import List
from app.models import Task, TaskStatus
from app.database import db

router = APIRouter()

@router.get("/tasks", response_model=List[Task])
async def get_tasks():
    cursor = db.tasks.find({"status": {"$ne": TaskStatus.Deleted}})
    tasks_list = []
    async for document in cursor:
        document["id"] = str(document["_id"])
        tasks_list.append(Task(**document))
    return tasks_list