from fastapi import APIRouter, HTTPException, status
from app.models import User, UserCreate
from app.database import db
from app.auth import get_password_hash

router = APIRouter()

@router.post("/register", response_model=User)
async def register(user_create: UserCreate):
    existing_user = await db.users.find_one({"email": user_create.email})
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    hashed_password = get_password_hash(user_create.password)
    user_doc = {
        "name": user_create.name,
        "email": user_create.email,
        "hashed_password": hashed_password,
    }
    result = await db.users.insert_one(user_doc)
    new_user = await db.users.find_one({"_id": result.inserted_id})
    new_user["id"] = str(new_user["_id"])
    new_user.pop("hashed_password", None)
    return User(**new_user)