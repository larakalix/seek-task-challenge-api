from pydantic import BaseModel
from enum import Enum

class TaskStatus(str, Enum):
    Todo = "to-do"
    InProgress = "in-progress"
    Done = "done"
    Deleted = "deleted"

class TaskBase(BaseModel):
    title: str
    description: str

class TaskCreate(TaskBase):
    pass

class TaskUpdate(BaseModel):
    title: str
    description: str
    status: TaskStatus

class Task(TaskBase):
    id: str
    status: TaskStatus