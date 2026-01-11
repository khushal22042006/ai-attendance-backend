from typing import Optional
from datetime import datetime
from bson import ObjectId
from pydantic import BaseModel, Field, ConfigDict, field_validator

# --- FIXED: Import shared types from base ---
from .base import PyObjectId, AttendanceStatus

class AttendanceRecordCreate(BaseModel):
    session_id: PyObjectId
    student_id: str
    status: AttendanceStatus = AttendanceStatus.PRESENT
    confidence: float = Field(..., ge=0.0, le=1.0)
    image_path: Optional[str] = None
    marked_at: datetime = Field(default_factory=datetime.utcnow)

    @field_validator('session_id')
    @classmethod
    def validate_session_id(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid session_id format")
        return str(v)

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "session_id": "65d5f8a9b4c7e12f34567890",
                "student_id": "BCA2023_045",
                "status": "present",
                "confidence": 0.91,
                "image_path": "/proofs/session1/img1.jpg",
                "marked_at": "2025-01-10T10:12:00"
            }
        }
    )

class AttendanceRecordUpdate(BaseModel):
    status: Optional[AttendanceStatus] = None
    confidence: Optional[float] = Field(None, ge=0.0, le=1.0)
    image_path: Optional[str] = None

class AttendanceRecordResponse(BaseModel):
    # Map MongoDB _id to id
    id: PyObjectId = Field(alias="_id")
    session_id: str
    student_id: str
    status: AttendanceStatus
    confidence: float
    image_path: Optional[str]
    marked_at: datetime

    model_config = ConfigDict(
        populate_by_name=True,
        from_attributes=True,
        json_schema_extra={
            "example": {
                "id": "65d5f8a9b4c7e12f34567891",
                "session_id": "65d5f8a9b4c7e12f34567890",
                "student_id": "BCA2023_045",
                "status": "present",
                "confidence": 0.91,
                "marked_at": "2025-01-10T10:12:00"
            }
        }
    )

class AttendanceRecordInDB(BaseModel):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    session_id: PyObjectId
    student_id: str
    status: AttendanceStatus
    confidence: float
    image_path: Optional[str] = None
    marked_at: datetime = Field(default_factory=datetime.utcnow)

    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True
    )