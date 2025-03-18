import os
from motor.motor_asyncio import AsyncIOMotorClient

MONGO_URL = os.environ.get("MONGO_URL")

if not MONGO_URL:
    raise ValueError("MONGO_URL environment variable not set!")

client = AsyncIOMotorClient(MONGO_URL)
db = client.tasks_db

user_collection = db.users
task_collection = db.tasks