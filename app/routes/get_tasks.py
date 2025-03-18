from fastapi import APIRouter
from typing import List
from app.models import Task, TaskStatus
from app.data import tasks

router = APIRouter()

@router.get("/tasks", response_model=List[Task])
def get_tasks():
    return [task for task in tasks if task.status != TaskStatus.Deleted]