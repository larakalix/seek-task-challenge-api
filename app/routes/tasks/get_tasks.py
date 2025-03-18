from fastapi import APIRouter, Depends
from typing import List
from app.models.task_model import Task
from app.dependencies import get_task_query_handler

router = APIRouter()

@router.get("/tasks", response_model=List[Task])
async def get_tasks(query_handler = Depends(get_task_query_handler)):
    tasks_list = await query_handler.get_tasks()
    return tasks_list