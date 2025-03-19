from fastapi import APIRouter, HTTPException, status
from app.models.user_model import UserLogin
from app.database import user_collection
from app.auth_helpers import create_access_token, verify_password, TokenData

router = APIRouter()

@router.post("/login")
async def login(user: UserLogin):
    user_doc = await user_collection.find_one({"email": user.email})
    # or not verify_password(user.password, user_doc["hashed_password"])
    if not user_doc or not verify_password(user.password, user_doc["hashed_password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    token_data = TokenData(
        user_id=str(user_doc["_id"]),
        email=user_doc["email"],
        name=user_doc.get("name", user_doc["email"])
    )
    
    token = create_access_token(user_data=token_data)
    
    return {
        "id": str(user_doc["_id"]),
        "name": user_doc.get("name", user_doc["email"]),
        "email": user_doc["email"],
        "token": token
    }