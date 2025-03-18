from fastapi import APIRouter, HTTPException, status
from datetime import timedelta
from app.models import User, UserCreate, UserLogin
from app.database import db
from app.auth import get_password_hash, verify_password, create_access_token, ACCESS_TOKEN_EXPIRE_MINUTES

router = APIRouter()

@router.post("/auth/register", response_model=User)
async def register(user_create: UserCreate):
    existing_user = await db.users.find_one({"email": user_create.email})
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    hashed_password = get_password_hash(user_create.password)
    user_doc = {
        "email": user_create.email,
        "hashed_password": hashed_password,
    }
    result = await db.users.insert_one(user_doc)
    new_user = await db.users.find_one({"_id": result.inserted_id})
    new_user["id"] = str(new_user["_id"])
    new_user.pop("hashed_password", None)  # Remove hashed password from response
    return User(**new_user)

@router.post("/auth/login")
async def login(user: UserLogin):
    user_doc = await db.users.find_one({"email": user.email})
    if not user_doc or not verify_password(user.password, user_doc["hashed_password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user_doc["email"]}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}