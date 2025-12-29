# backend/src/routes/attendance_record_routes.py
from typing import List
from fastapi import APIRouter, HTTPException
from models.attendence_record_model import (
    AttendanceRecordCreate, 
    AttendanceRecordResponse, 
    AttendanceRecordUpdate
)
from controllers.attendance_record_controller import (
    create_attendance_record,
    get_attendance_record,
    get_all_records,
    get_records_by_session,
    get_records_by_student,
    get_records_by_student_and_class,
    update_attendance_record,
    bulk_create_attendance_records,
    delete_attendance_record
)

router = APIRouter()

@router.post("/", response_model=AttendanceRecordResponse)
async def create_attendance_record_route(record_data: AttendanceRecordCreate):
    """Create a new attendance record"""
    return await create_attendance_record(record_data)

@router.post("/bulk", response_model=list[AttendanceRecordResponse])
async def bulk_create_attendance_records_route(records_data: List[AttendanceRecordCreate]):
    """Create multiple attendance records"""
    return await bulk_create_attendance_records(records_data)

@router.get("/{record_id}", response_model=AttendanceRecordResponse)
async def get_attendance_record_route(record_id: str):
    """Get attendance record by ID"""
    return await get_attendance_record(record_id)

@router.get("/", response_model=list[AttendanceRecordResponse])
async def get_all_records_route():
    """Get all attendance records"""
    return await get_all_records()

@router.get("/session/{session_id}", response_model=list[AttendanceRecordResponse])
async def get_records_by_session_route(session_id: str):
    """Get all attendance records for a session"""
    return await get_records_by_session(session_id)

@router.get("/student/{student_id}", response_model=list[AttendanceRecordResponse])
async def get_records_by_student_route(student_id: str):
    """Get all attendance records for a student"""
    return await get_records_by_student(student_id)

@router.get("/student/{student_id}/class/{class_id}", response_model=list[AttendanceRecordResponse])
async def get_records_by_student_and_class_route(student_id: str, class_id: str):
    """Get attendance records for a student in a specific class"""
    return await get_records_by_student_and_class(student_id, class_id)

@router.put("/{record_id}", response_model=AttendanceRecordResponse)
async def update_attendance_record_route(record_id: str, record_data: AttendanceRecordUpdate):
    """Update attendance record by ID"""
    return await update_attendance_record(record_id, record_data)

@router.delete("/{record_id}")
async def delete_attendance_record_route(record_id: str):
    """Delete attendance record by ID"""
    return await delete_attendance_record(record_id)
