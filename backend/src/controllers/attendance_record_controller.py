# backend/src/controllers/attendance_record_controller.py
from typing import List
from datetime import datetime
from bson import ObjectId
from fastapi import HTTPException
from models.attendence_record_model import (
    AttendanceRecordCreate, 
    AttendanceRecordResponse, 
    AttendanceRecordUpdate, 
    AttendanceRecordInDB,
    AttendanceStatus
)
from config.db_connect import get_mongo_collection


async def create_attendance_record(record_data: AttendanceRecordCreate) -> AttendanceRecordResponse:
    """
    Create a new attendance record
    """
    collection = get_mongo_collection("attendance_records")
    
    # Check if record already exists for this session and student
    existing_record = await collection.find_one({
        "session_id": record_data.session_id,
        "student_id": record_data.student_id
    })
    
    if existing_record:
        raise HTTPException(status_code=400, detail="Attendance record already exists for this session and student")
    
    # Create record document
    record_doc = {
        "session_id": record_data.session_id,
        "student_id": record_data.student_id,
        "status": record_data.status,
        "marked_at": record_data.marked_at or datetime.utcnow(),
        "marked_by": record_data.marked_by,
        "verification_method": record_data.verification_method,
        "confidence_score": record_data.confidence_score,
        "notes": record_data.notes,
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow()
    }
    
    # Insert into database
    result = await collection.insert_one(record_doc)
    
    # Return created record
    created_record = await collection.find_one({"_id": result.inserted_id})
    return AttendanceRecordInDB(**created_record)


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


async def get_records_by_session(session_id: str) -> List[AttendanceRecordResponse]:
    """
    Get all attendance records for a session
    """
    collection = get_mongo_collection("attendance_records")
    
    records = []
    async for record in collection.find({"session_id": session_id}):
        records.append(AttendanceRecordInDB(**record))
    
    return records


async def get_records_by_student(student_id: str) -> List[AttendanceRecordResponse]:
    """
    Get all attendance records for a student
    """
    collection = get_mongo_collection("attendance_records")
    
    records = []
    async for record in collection.find({"student_id": student_id}):
        records.append(AttendanceRecordInDB(**record))
    
    return records


async def get_records_by_student_and_class(student_id: str, class_id: str) -> List[AttendanceRecordResponse]:
    """
    Get attendance records for a student in a specific class
    """
    collection = get_mongo_collection("attendance_records")
    
    # Get all sessions for the class
    session_collection = get_mongo_collection("attendance_sessions")
    sessions = []
    async for session in session_collection.find({"class_id": class_id}):
        sessions.append(str(session["_id"]))
    
    # Get records for student in those sessions
    records = []
    async for record in collection.find({
        "student_id": student_id,
        "session_id": {"$in": sessions}
    }):
        records.append(AttendanceRecordInDB(**record))
    
    return records


async def get_all_records() -> List[AttendanceRecordResponse]:
    """
    Get all attendance records
    """
    collection = get_mongo_collection("attendance_records")
    
    records = []
    async for record in collection.find():
        records.append(AttendanceRecordInDB(**record))
    
    return records


async def update_attendance_record(record_id: str, record_data: AttendanceRecordUpdate) -> AttendanceRecordResponse:
    """
    Update attendance record by ID
    """
    collection = get_mongo_collection("attendance_records")
    
    if not ObjectId.is_valid(record_id):
        raise HTTPException(status_code=400, detail="Invalid record ID format")
    
    # Check if record exists
    existing_record = await collection.find_one({"_id": ObjectId(record_id)})
    if not existing_record:
        raise HTTPException(status_code=404, detail="Attendance record not found")
    
    # Prepare update data
    update_data = {k: v for k, v in record_data.dict().items() if v is not None}
    
    if not update_data:
        raise HTTPException(status_code=400, detail="No data provided for update")
    
    update_data["updated_at"] = datetime.utcnow()
    
    # Update record in database
    await collection.update_one(
        {"_id": ObjectId(record_id)},
        {"$set": update_data}
    )
    
    # Return updated record
    updated_record = await collection.find_one({"_id": ObjectId(record_id)})
    return AttendanceRecordInDB(**updated_record)


async def bulk_create_attendance_records(records_data: List[AttendanceRecordCreate]) -> List[AttendanceRecordResponse]:
    """
    Create multiple attendance records in bulk
    """
    collection = get_mongo_collection("attendance_records")
    
    records_to_insert = []
    for record_data in records_data:
        # Create record document
        record_doc = {
            "session_id": record_data.session_id,
            "student_id": record_data.student_id,
            "status": record_data.status,
            "marked_at": record_data.marked_at or datetime.utcnow(),
            "marked_by": record_data.marked_by,
            "verification_method": record_data.verification_method,
            "confidence_score": record_data.confidence_score,
            "notes": record_data.notes,
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        }
        records_to_insert.append(record_doc)
    
    # Insert in bulk
    if records_to_insert:
        result = await collection.insert_many(records_to_insert)
        
        # Return created records
        created_records = []
        for inserted_id in result.inserted_ids:
            record = await collection.find_one({"_id": inserted_id})
            created_records.append(AttendanceRecordInDB(**record))
        
        return created_records
    
    return []


async def delete_attendance_record(record_id: str) -> dict:
    """
    Delete attendance record by ID
    """
    collection = get_mongo_collection("attendance_records")
    
    if not ObjectId.is_valid(record_id):
        raise HTTPException(status_code=400, detail="Invalid record ID format")
    
    # Check if record exists
    existing_record = await collection.find_one({"_id": ObjectId(record_id)})
    if not existing_record:
        raise HTTPException(status_code=404, detail="Attendance record not found")
    
    # Delete record
    result = await collection.delete_one({"_id": ObjectId(record_id)})
    
    if result.deleted_count == 1:
        return {"message": "Attendance record deleted successfully"}
    else:
        raise HTTPException(status_code=500, detail="Failed to delete attendance record")