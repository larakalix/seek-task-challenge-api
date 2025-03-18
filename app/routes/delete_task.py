from fastapi import APIRouter, HTTPException, Depends
from app.auth import verify_token
from app.models import Task, TaskStatus
from app.database import db
from bson import ObjectId

router = APIRouter(dependencies=[Depends(verify_token)])

@router.delete("/tasks/{task_id}", response_model=Task)
async def soft_delete_task(task_id: str):
    try:
        obj_id = ObjectId(task_id)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid task ID format")
    
    existing_task = await db.tasks.find_one({"_id": obj_id})
    if existing_task is None or existing_task.get("status") == TaskStatus.Deleted:
        raise HTTPException(status_code=404, detail="Task not found")
    
    await db.tasks.update_one({"_id": obj_id}, {"$set": {"status": TaskStatus.Deleted}})
    deleted_task = await db.tasks.find_one({"_id": obj_id})
    deleted_task["id"] = str(deleted_task["_id"])
    return Task(**deleted_task)