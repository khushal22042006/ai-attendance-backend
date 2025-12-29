from typing import Optional
from datetime import date, time, datetime
from bson import ObjectId
from pydantic import BaseModel, Field, ConfigDict, field_validator
from enum import Enum
from .user_model import PyObjectId


class SessionStatus(str, Enum):
    SCHEDULED = "scheduled"
    ONGOING = "ongoing"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


class AttendanceSessionCreate(BaseModel):
    class_id: PyObjectId
    subject: str
    teacher_id: PyObjectId
    period: str
    date: date
    start_time: str  # Using string for time to match your sample
    end_time: str    # Using string for time to match your sample
    status: SessionStatus = SessionStatus.SCHEDULED

    @field_validator('class_id', 'teacher_id')
    @classmethod
    def validate_object_ids(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid ObjectId format")
        return str(v)

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "class_id": "65d5f8a9b4c7e12f34567892",
                "subject": "AI",
                "teacher_id": "65d5f8a9b4c7e12f34567893",
                "period": "1",
                "date": "2025-01-10",
                "start_time": "10:00",
                "end_time": "10:45",
                "status": "scheduled"
            }
        }
    )


class AttendanceSessionUpdate(BaseModel):
    subject: Optional[str] = None
    teacher_id: Optional[PyObjectId] = None
    period: Optional[str] = None
    start_time: Optional[str] = None
    end_time: Optional[str] = None
    status: Optional[SessionStatus] = None


class AttendanceSessionResponse(BaseModel):
    id: str
    class_id: str
    subject: str
    teacher_id: str
    period: str
    date: date
    start_time: str
    end_time: str
    status: SessionStatus
    created_at: datetime

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "id": "65d5f8a9b4c7e12f34567890",
                "class_id": "65d5f8a9b4c7e12f34567892",
                "subject": "AI",
                "teacher_id": "65d5f8a9b4c7e12f34567893",
                "period": "1",
                "date": "2025-01-10",
                "start_time": "10:00",
                "end_time": "10:45",
                "status": "completed",
                "created_at": "2025-01-09T14:30:00"
            }
        }
    )


class AttendanceSessionInDB(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    class_id: PyObjectId
    subject: str
    teacher_id: PyObjectId
    period: str
    date: date
    start_time: str
    end_time: str
    status: SessionStatus
    created_at: datetime = Field(default_factory=datetime.utcnow)

    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
        json_schema_extra={
            "example": {
                "_id": "65d5f8a9b4c7e12f34567890",
                "class_id": "65d5f8a9b4c7e12f34567892",
                "subject": "AI",
                "teacher_id": "65d5f8a9b4c7e12f34567893",
                "period": "1",
                "date": "2025-01-10",
                "start_time": "10:00",
                "end_time": "10:45",
                "status": "completed",
                "created_at": "2025-01-09T14:30:00"
            }
        }
    )