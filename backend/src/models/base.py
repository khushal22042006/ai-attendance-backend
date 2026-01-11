# backend/src/models/base.py
from typing import Annotated, Optional, List
from pydantic import BeforeValidator
from enum import Enum

PyObjectId = Annotated[str, BeforeValidator(str)]

class UserRole(str, Enum):
    TEACHER = "teacher"
    STUDENT = "student"
    ADMIN = "admin"

class AttendanceStatus(str, Enum):
    PRESENT = "present"
    ABSENT = "absent"
    LATE = "late"
    LEAVE = "leave"

# Add this for session tracking
class SessionStatus(str, Enum):
    SCHEDULED = "scheduled"
    ONGOING = "ongoing"
    COMPLETED = "completed"
    CANCELLED = "cancelled"