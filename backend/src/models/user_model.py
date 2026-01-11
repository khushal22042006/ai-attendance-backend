# backend/src/models/user_model.py
from typing import Optional
from datetime import datetime
from pydantic import BaseModel, EmailStr, Field, ConfigDict

# Import the shared types from base.py
from .base import PyObjectId, UserRole

# --- 1. Auth Specific Models ---

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None

class UserLogin(BaseModel):
    email: EmailStr  # Fixed typo: changed EmailStra to EmailStr
    password: str

# New Model to bypass the 'FieldInfo' attribute error in Python 3.13
class UserLoginRequest(BaseModel):
    username: str  # We use 'username' to stay compatible with OAuth2 logic
    password: str

# --- 2. User Management Models ---

class UserCreate(BaseModel):
    name: str = Field(..., min_length=2, max_length=100)
    email: EmailStr
    password: str = Field(..., min_length=6)
    role: UserRole = UserRole.STUDENT

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "name": "Rahul Sharma",
                "email": "rahul@gmail.com",
                "password": "securepassword123",
                "role": "student"
            }
        }
    )

class UserUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=2, max_length=100)
    email: Optional[EmailStr] = None
    role: Optional[UserRole] = None
    password: Optional[str] = None

class UserResponse(BaseModel):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    name: str
    email: EmailStr
    role: UserRole
    created_at: datetime
    google_id: Optional[str] = None

    model_config = ConfigDict(
        populate_by_name=True,
        from_attributes=True,
        json_schema_extra={
            "example": {
                "_id": "507f1f77bcf86cd799439011",
                "name": "Rahul Sharma",
                "email": "rahul@gmail.com",
                "role": "teacher",
                "created_at": "2025-01-01T10:00:00"
            }
        }
    )

# --- 3. Database Model ---

class UserInDB(BaseModel):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    name: str
    email: EmailStr
    hashed_password: Optional[str] = None
    role: UserRole
    created_at: datetime
    google_id: Optional[str] = None

    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True
    )