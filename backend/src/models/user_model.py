from typing import Optional
from datetime import datetime
from bson import ObjectId
from pydantic import BaseModel, EmailStr, Field, ConfigDict
from enum import Enum


class UserRole(str, Enum):
    TEACHER = "teacher"
    STUDENT = "student"
    ADMIN = "admin"


# Pydantic model for creating a user
class UserCreate(BaseModel):
    name: str = Field(..., min_length=2, max_length=100)
    email: EmailStr
    password: str = Field(..., min_length=6)
    role: UserRole = UserRole.TEACHER

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "name": "Rahul Sharma",
                "email": "rahul@gmail.com",
                "password": "securepassword123",
                "role": "teacher"
            }
        }
    )


# Pydantic model for updating a user
class UserUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=2, max_length=100)
    email: Optional[EmailStr] = None
    role: Optional[UserRole] = None

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "name": "Rahul Sharma Updated",
                "email": "rahul.updated@gmail.com",
                "role": "teacher"
            }
        }
    )


# Pydantic model for response (without password)
class UserResponse(BaseModel):
    id: str
    name: str
    email: EmailStr
    role: UserRole
    created_at: datetime

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "id": "507f1f77bcf86cd799439011",
                "name": "Rahul Sharma",
                "email": "rahul@gmail.com",
                "role": "teacher",
                "created_at": "2025-01-01T10:00:00"
            }
        }
    )


# Pydantic model for database (with MongoDB ObjectId)
class UserInDB(BaseModel):
    id: str = Field(..., alias="_id")
    name: str
    email: EmailStr
    password: str  # Hashed password
    role: UserRole
    created_at: datetime

    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
        json_schema_extra={
            "example": {
                "_id": "507f1f77bcf86cd799439011",
                "name": "Rahul Sharma",
                "email": "rahul@gmail.com",
                "password": "hashed_password",
                "role": "teacher",
                "created_at": "2025-01-01T10:00:00"
            }
        }
    )


# Helper function to convert ObjectId to string
class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid objectid")
        return ObjectId(v)

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(type="string")