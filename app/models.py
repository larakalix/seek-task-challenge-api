from pydantic import BaseModel, field_validator
from enum import Enum

class TaskStatus(str, Enum):
    Todo = "to-do"
    InProgress = "in-progress"
    Done = "done"
    Deleted = "deleted"

class TaskBase(BaseModel):
    title: str
    description: str

    @field_validator("title")
    def check_title(cls, v):
        if v is None or not v.strip():
            raise ValueError("Title must not be empty")
        return v

    @field_validator("description")
    def check_description(cls, v):
        if v is None or not v.strip():
            raise ValueError("Description must not be empty")
        return v

class TaskCreate(TaskBase):
    # Inherits the validations from TaskBase
    pass

class TaskUpdate(BaseModel):
    title: str
    description: str
    status: TaskStatus

    @field_validator("title")
    def check_title(cls, v):
        if v is None or not v.strip():
            raise ValueError("Title must not be empty")
        return v

    @field_validator("description")
    def check_description(cls, v):
        if v is None or not v.strip():
            raise ValueError("Description must not be empty")
        return v

class Task(TaskBase):
    id: str
    status: TaskStatus