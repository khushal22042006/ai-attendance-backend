# backend/src/routes/attendance_session_routes.py
from fastapi import APIRouter, HTTPException
from models.attendance_session_model import (
    AttendanceSessionCreate, 
    AttendanceSessionResponse, 
    AttendanceSessionUpdate
)
from controllers.attendance_session_controller import (
    create_attendance_session,
    get_attendance_session,
    get_all_sessions,
    get_sessions_by_class,
    get_active_sessions,
    update_attendance_session,
    start_attendance_session,
    end_attendance_session,
    delete_attendance_session
)

router = APIRouter()

@router.post("/", response_model=AttendanceSessionResponse)
async def create_attendance_session_route(session_data: AttendanceSessionCreate):
    """Create a new attendance session"""
    return await create_attendance_session(session_data)

@router.get("/{session_id}", response_model=AttendanceSessionResponse)
async def get_attendance_session_route(session_id: str):
    """Get attendance session by ID"""
    return await get_attendance_session(session_id)

@router.get("/", response_model=list[AttendanceSessionResponse])
async def get_all_sessions_route():
    """Get all attendance sessions"""
    return await get_all_sessions()

@router.get("/class/{class_id}", response_model=list[AttendanceSessionResponse])
async def get_sessions_by_class_route(class_id: str):
    """Get all attendance sessions for a class"""
    return await get_sessions_by_class(class_id)

@router.get("/active/all", response_model=list[AttendanceSessionResponse])
async def get_active_sessions_route():
    """Get all active attendance sessions"""
    return await get_active_sessions()

@router.put("/{session_id}", response_model=AttendanceSessionResponse)
async def update_attendance_session_route(session_id: str, session_data: AttendanceSessionUpdate):
    """Update attendance session by ID"""
    return await update_attendance_session(session_id, session_data)

@router.post("/{session_id}/start", response_model=AttendanceSessionResponse)
async def start_attendance_session_route(session_id: str):
    """Start an attendance session"""
    return await start_attendance_session(session_id)

@router.post("/{session_id}/end", response_model=AttendanceSessionResponse)
async def end_attendance_session_route(session_id: str):
    """End an attendance session"""
    return await end_attendance_session(session_id)

@router.delete("/{session_id}")
async def delete_attendance_session_route(session_id: str):
    """Delete attendance session by ID"""
    return await delete_attendance_session(session_id)