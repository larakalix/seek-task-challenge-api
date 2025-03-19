from fastapi import HTTPException
from app.models.task_model import TaskCreate, TaskUpdate, TaskStatus
from motor.motor_asyncio import AsyncIOMotorDatabase
from bson import ObjectId

class TaskCommandHandler:
    def __init__(self, db: AsyncIOMotorDatabase):
        self.collection = db.tasks

    async def create_task(self, task_create: TaskCreate, user_id: str, user_name: str) -> dict:        
        new_task = {
            "title": task_create.title,
            "description": task_create.description,
            "status": TaskStatus.Todo,
            "user_id": ObjectId(user_id),
            "user_name": user_name
        }
        result = await self.collection.insert_one(new_task)
        created_task = await self.collection.find_one({"_id": result.inserted_id})
        created_task["id"] = str(created_task["_id"])
        created_task["user_id"] = str(created_task["user_id"])
        return created_task

    async def update_task(self, task_id: str, task_update: TaskUpdate, user_id: str) -> dict:
        try:
            obj_id = ObjectId(task_id)
        except Exception:
            raise HTTPException(status_code=400, detail="Invalid task ID format")
        
        existing_task = await self.collection.find_one({"_id": obj_id})
        
        if str(existing_task.get("user_id")) != user_id:
            raise HTTPException(status_code=403, detail="Unauthorized: Task does not belong to user")
        
        if not existing_task  or existing_task.get("status") == TaskStatus.Deleted:
            raise HTTPException(status_code=404, detail="Task not found")
        
        updated_data = task_update.dict()
        await self.collection.update_one({"_id": obj_id}, {"$set": updated_data})
        updated_task = await self.collection.find_one({"_id": obj_id})
        updated_task["id"] = str(updated_task["_id"])
        updated_task["user_id"] = str(updated_task["user_id"])
        return updated_task

    async def delete_task(self, task_id: str, user_id: str) -> dict:
        try:
            obj_id = ObjectId(task_id)
        except Exception:
            raise HTTPException(status_code=400, detail="Invalid task ID format")
        
        existing_task = await self.collection.find_one({"_id": obj_id})
        
        if str(existing_task.get("user_id")) != user_id:
            raise HTTPException(status_code=403, detail="Unauthorized: Task does not belong to user")
        
        if not existing_task or existing_task.get("status") == TaskStatus.Deleted:
            raise HTTPException(status_code=404, detail="Task not found")
        
        await self.collection.update_one({"_id": obj_id}, {"$set": {"status": TaskStatus.Deleted}})
        deleted_task = await self.collection.find_one({"_id": obj_id})
        deleted_task["id"] = str(deleted_task["_id"])
        deleted_task["user_id"] = str(deleted_task["user_id"])
        return deleted_task
