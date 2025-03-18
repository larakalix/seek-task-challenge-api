from app.models import TaskCreate, TaskUpdate, TaskStatus
from motor.motor_asyncio import AsyncIOMotorDatabase
from bson import ObjectId
from fastapi import HTTPException

class TaskRepository:
    def __init__(self, db: AsyncIOMotorDatabase):
        self.collection = db.tasks

    async def get_tasks(self):
        cursor = self.collection.find({"status": {"$ne": TaskStatus.Deleted}})
        tasks_list = []
        async for document in cursor:
            document["id"] = str(document["_id"])
            tasks_list.append(document)
        return tasks_list

    async def create_task(self, task_create: TaskCreate):
        new_task = {
            "title": task_create.title,
            "description": task_create.description,
            "status": TaskStatus.Todo,
        }
        result = await self.collection.insert_one(new_task)
        created_task = await self.collection.find_one({"_id": result.inserted_id})
        created_task["id"] = str(created_task["_id"])
        return created_task

    async def update_task(self, task_id: str, task_update: TaskUpdate):
        try:
            obj_id = ObjectId(task_id)
        except Exception:
            raise HTTPException(status_code=400, detail="Invalid task ID format")
        
        existing_task = await self.collection.find_one({"_id": obj_id})
        if existing_task is None or existing_task.get("status") == TaskStatus.Deleted:
            raise HTTPException(status_code=404, detail="Task not found")
        
        updated_data = task_update.dict()
        await self.collection.update_one({"_id": obj_id}, {"$set": updated_data})
        updated_task = await self.collection.find_one({"_id": obj_id})
        updated_task["id"] = str(updated_task["_id"])
        return updated_task

    async def soft_delete_task(self, task_id: str):
        try:
            obj_id = ObjectId(task_id)
        except Exception:
            raise HTTPException(status_code=400, detail="Invalid task ID format")
        
        existing_task = await self.collection.find_one({"_id": obj_id})
        if existing_task is None or existing_task.get("status") == TaskStatus.Deleted:
            raise HTTPException(status_code=404, detail="Task not found")
        
        await self.collection.update_one({"_id": obj_id}, {"$set": {"status": TaskStatus.Deleted}})
        deleted_task = await self.collection.find_one({"_id": obj_id})
        deleted_task["id"] = str(deleted_task["_id"])
        return deleted_task
