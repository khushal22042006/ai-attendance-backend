# backend/src/controllers/student_controller.py
from typing import List
from datetime import datetime
from bson import ObjectId
from fastapi import HTTPException
from models.student_model import StudentCreate, StudentResponse, StudentUpdate, StudentInDB
from config.db_connect import get_mongo_collection


async def create_student(student_data: StudentCreate) -> StudentResponse:
    """
    Create a new student
    """
    collection = get_mongo_collection("students")
    
    # Check if student with same roll number exists
    existing_student = await collection.find_one({"roll_number": student_data.roll_number})
    if existing_student:
        raise HTTPException(status_code=400, detail="Student with this roll number already exists")
    
    # Create student document
    student_doc = {
        "user_id": student_data.user_id,
        "roll_number": student_data.roll_number,
        "class_ids": student_data.class_ids or [],
        "department": student_data.department,
        "year": student_data.year,
        "section": student_data.section,
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow()
    }
    
    # Insert into database
    result = await collection.insert_one(student_doc)
    
    # Return created student
    created_student = await collection.find_one({"_id": result.inserted_id})
    return StudentInDB(**created_student)


async def get_student(student_id: str) -> StudentResponse:
    """
    Get student by ID
    """
    collection = get_mongo_collection("students")
    
    if not ObjectId.is_valid(student_id):
        raise HTTPException(status_code=400, detail="Invalid student ID format")
    
    student = await collection.find_one({"_id": ObjectId(student_id)})
    
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    
    return StudentInDB(**student)


async def get_student_by_user_id(user_id: str) -> StudentResponse:
    """
    Get student by user ID
    """
    collection = get_mongo_collection("students")
    
    if not ObjectId.is_valid(user_id):
        raise HTTPException(status_code=400, detail="Invalid user ID format")
    
    student = await collection.find_one({"user_id": user_id})
    
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    
    return StudentInDB(**student)


async def get_students_by_class(class_id: str) -> List[StudentResponse]:
    """
    Get all students in a class
    """
    collection = get_mongo_collection("students")
    
    students = []
    async for student in collection.find({"class_ids": class_id}):
        students.append(StudentInDB(**student))
    
    return students


async def get_all_students() -> List[StudentResponse]:
    """
    Get all students
    """
    collection = get_mongo_collection("students")
    
    students = []
    async for student in collection.find():
        students.append(StudentInDB(**student))
    
    return students


async def update_student(student_id: str, student_data: StudentUpdate) -> StudentResponse:
    """
    Update student by ID
    """
    collection = get_mongo_collection("students")
    
    if not ObjectId.is_valid(student_id):
        raise HTTPException(status_code=400, detail="Invalid student ID format")
    
    # Check if student exists
    existing_student = await collection.find_one({"_id": ObjectId(student_id)})
    if not existing_student:
        raise HTTPException(status_code=404, detail="Student not found")
    
    # Check if roll number is being changed and if it already exists
    if student_data.roll_number and student_data.roll_number != existing_student.get("roll_number"):
        roll_number_exists = await collection.find_one({
            "roll_number": student_data.roll_number,
            "_id": {"$ne": ObjectId(student_id)}
        })
        if roll_number_exists:
            raise HTTPException(status_code=400, detail="Roll number already exists")
    
    # Prepare update data
    update_data = {k: v for k, v in student_data.dict().items() if v is not None}
    
    if not update_data:
        raise HTTPException(status_code=400, detail="No data provided for update")
    
    update_data["updated_at"] = datetime.utcnow()
    
    # Update student in database
    await collection.update_one(
        {"_id": ObjectId(student_id)},
        {"$set": update_data}
    )
    
    # Return updated student
    updated_student = await collection.find_one({"_id": ObjectId(student_id)})
    return StudentInDB(**updated_student)


async def delete_student(student_id: str) -> dict:
    """
    Delete student by ID
    """
    collection = get_mongo_collection("students")
    
    if not ObjectId.is_valid(student_id):
        raise HTTPException(status_code=400, detail="Invalid student ID format")
    
    # Check if student exists
    existing_student = await collection.find_one({"_id": ObjectId(student_id)})
    if not existing_student:
        raise HTTPException(status_code=404, detail="Student not found")
    
    # Remove student from all classes
    class_collection = get_mongo_collection("classes")
    await class_collection.update_many(
        {"student_ids": student_id},
        {"$pull": {"student_ids": student_id}}
    )
    
    # Delete student
    result = await collection.delete_one({"_id": ObjectId(student_id)})
    
    if result.deleted_count == 1:
        return {"message": "Student deleted successfully"}
    else:
        raise HTTPException(status_code=500, detail="Failed to delete student")