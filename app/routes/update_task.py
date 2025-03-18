from fastapi import APIRouter, HTTPException
from app.models import Task, TaskUpdate, TaskStatus
from app.database import db
from bson import ObjectId

router = APIRouter()

@router.put("/tasks/{task_id}", response_model=Task)
async def update_task(task_id: str, task_update: TaskUpdate):
    try:
        obj_id = ObjectId(task_id)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid task ID format")
    
    existing_task = await db.tasks.find_one({"_id": obj_id})
    if existing_task is None or existing_task.get("status") == TaskStatus.Deleted:
        raise HTTPException(status_code=404, detail="Task not found")
    
    updated_data = task_update.dict()
    await db.tasks.update_one({"_id": obj_id}, {"$set": updated_data})
    updated_task = await db.tasks.find_one({"_id": obj_id})
    updated_task["id"] = str(updated_task["_id"])
    return Task(**updated_task)