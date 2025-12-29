# backend/src/routes/student_routes.py
from fastapi import APIRouter, HTTPException
from models.student_model import StudentCreate, StudentResponse, StudentUpdate
from controllers.student_controller import (
    create_student,
    get_student,
    get_student_by_user_id,
    get_all_students,
    get_students_by_class,
    update_student,
    delete_student
)

router = APIRouter()

@router.post("/", response_model=StudentResponse)
async def create_student_route(student_data: StudentCreate):
    """Create a new student"""
    return await create_student(student_data)

@router.get("/{student_id}", response_model=StudentResponse)
async def get_student_route(student_id: str):
    """Get student by ID"""
    return await get_student(student_id)

@router.get("/user/{user_id}", response_model=StudentResponse)
async def get_student_by_user_route(user_id: str):
    """Get student by user ID"""
    return await get_student_by_user_id(user_id)

@router.get("/", response_model=list[StudentResponse])
async def get_all_students_route():
    """Get all students"""
    return await get_all_students()

@router.get("/class/{class_id}", response_model=list[StudentResponse])
async def get_students_by_class_route(class_id: str):
    """Get all students in a class"""
    return await get_students_by_class(class_id)

@router.put("/{student_id}", response_model=StudentResponse)
async def update_student_route(student_id: str, student_data: StudentUpdate):
    """Update student by ID"""
    return await update_student(student_id, student_data)

@router.delete("/{student_id}")
async def delete_student_route(student_id: str):
    """Delete student by ID"""
    return await delete_student(student_id)