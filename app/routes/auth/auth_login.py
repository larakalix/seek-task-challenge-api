from fastapi import APIRouter, HTTPException, status
from datetime import timedelta
from app.models.user_model import UserLogin
from app.database import user_collection
from app.auth_helpers import verify_password, create_access_token, ACCESS_TOKEN_EXPIRE_MINUTES

router = APIRouter()

@router.post("/login")
async def login(user: UserLogin):
    user_doc = await user_collection.find_one({"email": user.email})
    if not user_doc or not verify_password(user.password, user_doc["hashed_password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    token_data = {
        "sub": user_doc["email"],
        "id": str(user_doc["_id"]),
        "email": user_doc["email"],
        "name": user_doc.get("name", user_doc["email"])
    }
    
    token = create_access_token(
        data=token_data, expires_delta=access_token_expires
    )
    
    return {
        "id": str(user_doc["_id"]),
        "name": user_doc.get("name", user_doc["email"]),
        "email": user_doc["email"],
        "token": token
    }