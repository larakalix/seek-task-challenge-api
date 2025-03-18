from pydantic import BaseModel, EmailStr, field_validator
from enum import Enum

# --------------------
# User Models
# --------------------
class UserBase(BaseModel):
    name: str
    email: EmailStr

class UserCreate(UserBase):
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class User(UserBase):
    id: str

# --------------------
# Task Models
# --------------------
class TaskStatus(str, Enum):
    Todo = "to-do"
    InProgress = "in-progress"
    Done = "done"
    Deleted = "deleted"

class TaskBase(BaseModel):
    title: str
    description: str

    @field_validator("title")
    def validate_title(cls, value: str) -> str:
        if value is None or not value.strip():
            raise ValueError("Title must not be empty")
        return value

    @field_validator("description")
    def validate_description(cls, value: str) -> str:
        if value is None or not value.strip():
            raise ValueError("Description must not be empty")
        return value

class TaskCreate(TaskBase):
    pass

class TaskUpdate(TaskBase):
    status: TaskStatus

    @field_validator("status")
    def validate_status(cls, value: TaskStatus) -> TaskStatus:
        if value is None:
            raise ValueError("Status must not be null")
        return value

class Task(TaskUpdate):
    id: str