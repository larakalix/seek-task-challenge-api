from app.models.task_model import Task, TaskStatus
from motor.motor_asyncio import AsyncIOMotorDatabase

class TaskQueryHandler:
    def __init__(self, db: AsyncIOMotorDatabase):
        self.collection = db.tasks

    async def get_tasks(self) -> list:
        pipeline = [
            {"$match": {"status": {"$ne": TaskStatus.Deleted}}},
            {"$lookup": {
                "from": "users",
                "localField": "user_id",
                "foreignField": "_id",
                "as": "user_info"
            }},
            {"$unwind": "$user_info"},
            {"$addFields": {"user_name": "$user_info.name"}},
            {"$project": {"user_info": 0}}
        ]
        cursor = self.collection.aggregate(pipeline)
        tasks_list = []
        async for document in cursor:
            document["id"] = str(document["_id"])
            document["user_id"] = str(document["user_id"])
            tasks_list.append(document)
        return tasks_list
