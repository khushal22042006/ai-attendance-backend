# backend/src/controllers/attendance_session_controller.py
from typing import List
from datetime import datetime
from bson import ObjectId
from fastapi import HTTPException
from models.attendence_session_model import (
    AttendanceSessionCreate, 
    AttendanceSessionResponse, 
    AttendanceSessionUpdate, 
    AttendanceSessionInDB,
    SessionStatus
)
from config.db_connect import get_mongo_collection


async def create_attendance_session(session_data: AttendanceSessionCreate) -> AttendanceSessionResponse:
    """
    Create a new attendance session
    """
    collection = get_mongo_collection("attendance_sessions")
    
    # Create session document
    session_doc = {
        "class_id": session_data.class_id,
        "teacher_id": session_data.teacher_id,
        "session_name": session_data.session_name,
        "description": session_data.description,
        "scheduled_start": session_data.scheduled_start,
        "scheduled_end": session_data.scheduled_end,
        "actual_start": session_data.actual_start,
        "actual_end": session_data.actual_end,
        "status": session_data.status,
        "location": session_data.location,
        "qr_code_data": session_data.qr_code_data,
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow()
    }
    
    # Insert into database
    result = await collection.insert_one(session_doc)
    
    # Return created session
    created_session = await collection.find_one({"_id": result.inserted_id})
    return AttendanceSessionInDB(**created_session)


async def get_attendance_session(session_id: str) -> AttendanceSessionResponse:
    """
    Get attendance session by ID
    """
    collection = get_mongo_collection("attendance_sessions")
    
    if not ObjectId.is_valid(session_id):
        raise HTTPException(status_code=400, detail="Invalid session ID format")
    
    session = await collection.find_one({"_id": ObjectId(session_id)})
    
    if not session:
        raise HTTPException(status_code=404, detail="Attendance session not found")
    
    return AttendanceSessionInDB(**session)


async def get_sessions_by_class(class_id: str) -> List[AttendanceSessionResponse]:
    """
    Get all attendance sessions for a class
    """
    collection = get_mongo_collection("attendance_sessions")
    
    sessions = []
    async for session in collection.find({"class_id": class_id}):
        sessions.append(AttendanceSessionInDB(**session))
    
    return sessions


async def get_active_sessions() -> List[AttendanceSessionResponse]:
    """
    Get all active attendance sessions
    """
    collection = get_mongo_collection("attendance_sessions")
    
    sessions = []
    async for session in collection.find({"status": SessionStatus.ACTIVE}):
        sessions.append(AttendanceSessionInDB(**session))
    
    return sessions


async def get_all_sessions() -> List[AttendanceSessionResponse]:
    """
    Get all attendance sessions
    """
    collection = get_mongo_collection("attendance_sessions")
    
    sessions = []
    async for session in collection.find():
        sessions.append(AttendanceSessionInDB(**session))
    
    return sessions


async def update_attendance_session(session_id: str, session_data: AttendanceSessionUpdate) -> AttendanceSessionResponse:
    """
    Update attendance session by ID
    """
    collection = get_mongo_collection("attendance_sessions")
    
    if not ObjectId.is_valid(session_id):
        raise HTTPException(status_code=400, detail="Invalid session ID format")
    
    # Check if session exists
    existing_session = await collection.find_one({"_id": ObjectId(session_id)})
    if not existing_session:
        raise HTTPException(status_code=404, detail="Attendance session not found")
    
    # Prepare update data
    update_data = {k: v for k, v in session_data.dict().items() if v is not None}
    
    if not update_data:
        raise HTTPException(status_code=400, detail="No data provided for update")
    
    update_data["updated_at"] = datetime.utcnow()
    
    # Update session in database
    await collection.update_one(
        {"_id": ObjectId(session_id)},
        {"$set": update_data}
    )
    
    # Return updated session
    updated_session = await collection.find_one({"_id": ObjectId(session_id)})
    return AttendanceSessionInDB(**updated_session)


async def start_attendance_session(session_id: str) -> AttendanceSessionResponse:
    """
    Start an attendance session
    """
    collection = get_mongo_collection("attendance_sessions")
    
    if not ObjectId.is_valid(session_id):
        raise HTTPException(status_code=400, detail="Invalid session ID format")
    
    # Check if session exists
    existing_session = await collection.find_one({"_id": ObjectId(session_id)})
    if not existing_session:
        raise HTTPException(status_code=404, detail="Attendance session not found")
    
    # Update session status and actual start time
    update_data = {
        "status": SessionStatus.ACTIVE,
        "actual_start": datetime.utcnow(),
        "updated_at": datetime.utcnow()
    }
    
    await collection.update_one(
        {"_id": ObjectId(session_id)},
        {"$set": update_data}
    )
    
    # Return updated session
    updated_session = await collection.find_one({"_id": ObjectId(session_id)})
    return AttendanceSessionInDB(**updated_session)


async def end_attendance_session(session_id: str) -> AttendanceSessionResponse:
    """
    End an attendance session
    """
    collection = get_mongo_collection("attendance_sessions")
    
    if not ObjectId.is_valid(session_id):
        raise HTTPException(status_code=400, detail="Invalid session ID format")
    
    # Check if session exists
    existing_session = await collection.find_one({"_id": ObjectId(session_id)})
    if not existing_session:
        raise HTTPException(status_code=404, detail="Attendance session not found")
    
    # Update session status and actual end time
    update_data = {
        "status": SessionStatus.COMPLETED,
        "actual_end": datetime.utcnow(),
        "updated_at": datetime.utcnow()
    }
    
    await collection.update_one(
        {"_id": ObjectId(session_id)},
        {"$set": update_data}
    )
    
    # Return updated session
    updated_session = await collection.find_one({"_id": ObjectId(session_id)})
    return AttendanceSessionInDB(**updated_session)


async def delete_attendance_session(session_id: str) -> dict:
    """
    Delete attendance session by ID
    """
    collection = get_mongo_collection("attendance_sessions")
    
    if not ObjectId.is_valid(session_id):
        raise HTTPException(status_code=400, detail="Invalid session ID format")
    
    # Check if session exists
    existing_session = await collection.find_one({"_id": ObjectId(session_id)})
    if not existing_session:
        raise HTTPException(status_code=404, detail="Attendance session not found")
    
    # Delete session
    result = await collection.delete_one({"_id": ObjectId(session_id)})
    
    if result.deleted_count == 1:
        return {"message": "Attendance session deleted successfully"}
    else:
        raise HTTPException(status_code=500, detail="Failed to delete attendance session")