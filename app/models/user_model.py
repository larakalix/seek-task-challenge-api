from pydantic import BaseModel, EmailStr, field_validator

class UserBase(BaseModel):
    email: EmailStr
    password: str
    
    @field_validator("email")
    def validate_email(cls, value: EmailStr) -> EmailStr:
        if value is None:
            raise ValueError("Email must not be null")
        return value
    
    @field_validator("password")
    def validate_password(cls, value: str) -> str:
        if value is None or not value.strip():
            raise ValueError("Password must not be empty")
        return value

class UserCreate(UserBase):
    name: str
    
    @field_validator("name")
    def validate_name(cls, value: str) -> str:
        if value is None or not value.strip():
            raise ValueError("Name must not be empty")
        return value

class UserLogin(UserBase):
    pass

class User(UserBase):
    id: str

def user_serializer(user) -> dict:
    return {
        "id": str(user["_id"]),
        "username": user["username"],
        "email": user["email"]
    }