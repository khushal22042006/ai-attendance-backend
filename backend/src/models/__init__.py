# backend/src/models/__init__.py

from .user_model import *
from .attendance_record_model import *
from .attendance_session_model import *
from .class_model import *
from .face_embedding_model import *
from .student_model import *

# Export all models
__all__ = [
    # User models
    "UserCreate", "UserUpdate", "UserResponse", "UserInDB", "UserRole",
    
    # Attendance models
    "AttendanceRecordCreate", "AttendanceRecordUpdate", 
    "AttendanceRecordResponse", "AttendanceRecordInDB", "AttendanceStatus",
    
    # Session models
    "AttendanceSessionCreate", "AttendanceSessionUpdate",
    "AttendanceSessionResponse", "AttendanceSessionInDB", "SessionStatus",
    
    # Class models
    "ClassCreate", "ClassUpdate", "ClassResponse", "ClassInDB",
    
    # Face embedding models
    "FaceEmbeddingCreate", "FaceEmbeddingUpdate", 
    "FaceEmbeddingResponse", "FaceEmbeddingInDB",
    "FaceMatchRequest", "FaceMatchResponse",
    
    # Student models
    "StudentCreate", "StudentUpdate", "StudentResponse", "StudentInDB",
    "StudentAttendanceSummary"
]