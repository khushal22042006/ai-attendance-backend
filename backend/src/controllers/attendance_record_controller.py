from typing import List, Optional
from datetime import datetime
from bson import ObjectId
from fastapi import HTTPException
from models.attendance_record_model import (
    AttendanceRecordCreate,
    AttendanceRecordResponse,
    AttendanceRecordUpdate,
    AttendanceRecordInDB,
    AttendanceStatus
)
from config.db_connect import get_mongo_collection


class AttendanceRecordController:
    @staticmethod
    async def create_attendance_record(record_data: AttendanceRecordCreate) -> AttendanceRecordResponse:
        """
        Create a new attendance record
        """
        collection = get_mongo_collection("attendance_records")
        
        # Check if student exists
        students_collection = get_mongo_collection("students")
        student = await students_collection.find_one({"_id": ObjectId(record_data.student_id)})
        if not student:
            raise HTTPException(status_code=404, detail="Student not found")
        
        # Check if session exists
        sessions_collection = get_mongo_collection("attendance_sessions")
        session = await sessions_collection.find_one({"_id": ObjectId(record_data.session_id)})
        if not session:
            raise HTTPException(status_code=404, detail="Session not found")
        
        # Check for duplicate attendance
        existing_record = await collection.find_one({
            "student_id": record_data.student_id,
            "session_id": record_data.session_id
        })
        if existing_record:
            raise HTTPException(status_code=400, detail="Attendance already recorded for this session")
        
        # Create attendance record
        now = datetime.utcnow()
        record_doc = {
            "student_id": record_data.student_id,
            "session_id": record_data.session_id,
            "attendance_time": record_data.attendance_time or now,
            "status": record_data.status,
            "method": record_data.method,
            "confidence_score": record_data.confidence_score,
            "verified_by": record_data.verified_by,
            "notes": record_data.notes,
            "created_at": now,
            "updated_at": now
        }
        
        # Insert into database
        result = await collection.insert_one(record_doc)
        
        # Update attendance count in session
        await sessions_collection.update_one(
            {"_id": ObjectId(record_data.session_id)},
            {"$inc": {"attendance_count": 1}}
        )
        
        # Return created record
        created_record = await collection.find_one({"_id": result.inserted_id})
        return AttendanceRecordInDB(**created_record)

    @staticmethod
    async def get_attendance_record(record_id: str) -> AttendanceRecordResponse:
        """
        Get attendance record by ID
        """
        collection = get_mongo_collection("attendance_records")
        
        if not ObjectId.is_valid(record_id):
            raise HTTPException(status_code=400, detail="Invalid record ID format")
        
        record = await collection.find_one({"_id": ObjectId(record_id)})
        
        if not record:
            raise HTTPException(status_code=404, detail="Attendance record not found")
        
        return AttendanceRecordInDB(**record)

    @staticmethod
    async def get_attendance_by_session(session_id: str) -> List[AttendanceRecordResponse]:
        """
        Get all attendance records for a session
        """
        collection = get_mongo_collection("attendance_records")
        
        if not ObjectId.is_valid(session_id):
            raise HTTPException(status_code=400, detail="Invalid session ID format")
        
        records = []
        async for record in collection.find({"session_id": session_id}).sort("attendance_time", -1):
            records.append(AttendanceRecordInDB(**record))
        
        return records

    @staticmethod
    async def get_attendance_by_student(
        student_id: str, 
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None
    ) -> List[AttendanceRecordResponse]:
        """
        Get attendance records for a student with optional date range
        """