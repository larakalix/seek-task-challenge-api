from fastapi import APIRouter, HTTPException
from app.models import Task, TaskUpdate, TaskStatus
from app.data import tasks

router = APIRouter()

@router.put("/tasks/{task_id}", response_model=Task)
def update_task(task_id: str, task_update: TaskUpdate):
    for index, task in enumerate(tasks):
        if task.id == task_id:
            if task.status == TaskStatus.Deleted:
                raise HTTPException(status_code=404, detail="Task not found")
            updated_task = task.model_copy(update=task_update.model_dump())
            tasks[index] = updated_task
            return updated_task
    raise HTTPException(status_code=404, detail="Task not found")