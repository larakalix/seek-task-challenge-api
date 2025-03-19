from fastapi import APIRouter, Depends, HTTPException, Request
from typing import List
from app.models.task_model import Task
from app.dependencies import get_task_query_handler
from app.auth_helpers import get_session_from_request, TokenData
from app.database import db

router = APIRouter()

@router.get("/tasks", response_model=List[Task])
async def get_tasks(query_handler = Depends(get_task_query_handler)):
    tasks_list = await query_handler.get_tasks()
    return tasks_list

@router.get("/tasks/deleted", response_model=List[Task])
async def get_deleted_tasks(
    request: Request,
    query_handler = Depends(get_task_query_handler)
):
    session = await get_session_from_request(request)
    user_email = session.get("user_email")
    user_doc = await db.users.find_one({"email": user_email})
    
    if not user_doc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found"
        )
    
    user_id = str(user_doc["_id"])
    tasks_list = await query_handler.get_deleted_tasks(user_id)
    return tasks_list