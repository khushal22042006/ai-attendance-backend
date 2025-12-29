# backend/src/routes/class_routes.py
from fastapi import APIRouter, HTTPException
from models.class_model import ClassCreate, ClassResponse, ClassUpdate
from controllers.class_controller import (
    create_class,
    get_class,
    get_all_classes,
    get_classes_by_teacher,
    update_class,
    add_student_to_class,
    remove_student_from_class,
    delete_class
)

router = APIRouter()

@router.post("/", response_model=ClassResponse)
async def create_class_route(class_data: ClassCreate):
    """Create a new class"""
    return await create_class(class_data)

@router.get("/{class_id}", response_model=ClassResponse)
async def get_class_route(class_id: str):
    """Get class by ID"""
    return await get_class(class_id)

@router.get("/", response_model=list[ClassResponse])
async def get_all_classes_route():
    """Get all classes"""
    return await get_all_classes()

@router.get("/teacher/{teacher_id}", response_model=list[ClassResponse])
async def get_classes_by_teacher_route(teacher_id: str):
    """Get all classes for a teacher"""
    return await get_classes_by_teacher(teacher_id)

@router.put("/{class_id}", response_model=ClassResponse)
async def update_class_route(class_id: str, class_data: ClassUpdate):
    """Update class by ID"""
    return await update_class(class_id, class_data)

@router.post("/{class_id}/students/{student_id}", response_model=ClassResponse)
async def add_student_to_class_route(class_id: str, student_id: str):
    """Add student to class"""
    return await add_student_to_class(class_id, student_id)

@router.delete("/{class_id}/students/{student_id}", response_model=ClassResponse)
async def remove_student_from_class_route(class_id: str, student_id: str):
    """Remove student from class"""
    return await remove_student_from_class(class_id, student_id)

@router.delete("/{class_id}")
async def delete_class_route(class_id: str):
    """Delete class by ID"""
    return await delete_class(class_id)