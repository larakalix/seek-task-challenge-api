from fastapi import APIRouter, HTTPException
from app.models import Task, TaskStatus
from app.data import tasks

router = APIRouter()

@router.delete("/tasks/{task_id}", response_model=Task)
def soft_delete_task(task_id: str):
    for index, task in enumerate(tasks):
        if task.id == task_id:
            if task.status == TaskStatus.Deleted:
                raise HTTPException(status_code=404, detail="Task not found")
            deleted_task = task.copy(update={"status": TaskStatus.Deleted})
            tasks[index] = deleted_task
            return deleted_task
    raise HTTPException(status_code=404, detail="Task not found")