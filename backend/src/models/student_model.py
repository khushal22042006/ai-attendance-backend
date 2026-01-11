from typing import Optional
from datetime import datetime
from bson import ObjectId
from pydantic import BaseModel, Field, EmailStr, ConfigDict, field_validator

# --- CRITICAL FIX: Import from .base to avoid circular dependency ---
from .base import PyObjectId 

class StudentCreate(BaseModel):
    student_id: str = Field(..., pattern=r'^[A-Za-z0-9_]+$')
    name: str = Field(..., min_length=2, max_length=100)
    class_id: PyObjectId
    email: EmailStr
    registered_face: bool = False

    @field_validator('class_id')
    @classmethod
    def validate_class_id(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid class_id format")
        return str(v)

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "student_id": "BCA2023_045",
                "name": "Amit Kumar",
                "class_id": "65d5f8a9b4c7e12f34567892",
                "email": "amit@gmail.com",
                "registered_face": True
            }
        }
    )

class StudentUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=2, max_length=100)
    class_id: Optional[PyObjectId] = None
    email: Optional[EmailStr] = None
    registered_face: Optional[bool] = None

class StudentResponse(BaseModel):
    # Use PyObjectId here to handle MongoDB _id correctly
    id: PyObjectId = Field(alias="_id")
    student_id: str
    name: str
    class_id: str
    email: EmailStr
    registered_face: bool
    created_at: datetime

    model_config = ConfigDict(
        populate_by_name=True,
        from_attributes=True,
        json_schema_extra={
            "example": {
                "_id": "65d5f8a9b4c7e12f34567895",
                "student_id": "BCA2023_045",
                "name": "Amit Kumar",
                "class_id": "65d5f8a9b4c7e12f34567892",
                "email": "amit@gmail.com",
                "registered_face": True,
                "created_at": "2025-01-01T09:00:00"
            }
        }
    )

class StudentInDB(BaseModel):
    id: PyObjectId = Field(alias="_id", default=None)
    student_id: str
    name: str
    class_id: PyObjectId
    email: EmailStr
    registered_face: bool
    created_at: datetime = Field(default_factory=datetime.utcnow)

    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True
    )

class StudentAttendanceSummary(BaseModel):
    student_id: str
    name: str
    total_sessions: int
    attended_sessions: int
    attendance_percentage: float
    last_attended: Optional[datetime]