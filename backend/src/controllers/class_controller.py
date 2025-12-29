# backend/src/controllers/class_controller.py
from typing import List
from datetime import datetime
from bson import ObjectId
from fastapi import HTTPException
from models.class_model import ClassCreate, ClassResponse, ClassUpdate, ClassInDB
from config.db_connect import get_mongo_collection


async def create_class(class_data: ClassCreate) -> ClassResponse:
    """
    Create a new class
    """
    collection = get_mongo_collection("classes")
    
    # Check if class with same code exists
    existing_class = await collection.find_one({"class_code": class_data.class_code})
    if existing_class:
        raise HTTPException(status_code=400, detail="Class with this code already exists")
    
    # Create class document
    class_doc = {
        "class_name": class_data.class_name,
        "class_code": class_data.class_code,
        "description": class_data.description,
        "teacher_id": class_data.teacher_id,
        "student_ids": class_data.student_ids or [],
        "schedule": class_data.schedule,
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow()
    }
    
    # Insert into database
    result = await collection.insert_one(class_doc)
    
    # Return created class
    created_class = await collection.find_one({"_id": result.inserted_id})
    return ClassInDB(**created_class)


async def get_class(class_id: str) -> ClassResponse:
    """
    Get class by ID
    """
    collection = get_mongo_collection("classes")
    
    if not ObjectId.is_valid(class_id):
        raise HTTPException(status_code=400, detail="Invalid class ID format")
    
    class_obj = await collection.find_one({"_id": ObjectId(class_id)})
    
    if not class_obj:
        raise HTTPException(status_code=404, detail="Class not found")
    
    return ClassInDB(**class_obj)


async def get_classes_by_teacher(teacher_id: str) -> List[ClassResponse]:
    """
    Get all classes for a teacher
    """
    collection = get_mongo_collection("classes")
    
    if not ObjectId.is_valid(teacher_id):
        raise HTTPException(status_code=400, detail="Invalid teacher ID format")
    
    classes = []
    async for class_obj in collection.find({"teacher_id": teacher_id}):
        classes.append(ClassInDB(**class_obj))
    
    return classes


async def get_all_classes() -> List[ClassResponse]:
    """
    Get all classes
    """
    collection = get_mongo_collection("classes")
    
    classes = []
    async for class_obj in collection.find():
        classes.append(ClassInDB(**class_obj))
    
    return classes


async def update_class(class_id: str, class_data: ClassUpdate) -> ClassResponse:
    """
    Update class by ID
    """
    collection = get_mongo_collection("classes")
    
    if not ObjectId.is_valid(class_id):
        raise HTTPException(status_code=400, detail="Invalid class ID format")
    
    # Check if class exists
    existing_class = await collection.find_one({"_id": ObjectId(class_id)})
    if not existing_class:
        raise HTTPException(status_code=404, detail="Class not found")
    
    # Prepare update data
    update_data = {k: v for k, v in class_data.dict().items() if v is not None}
    
    if not update_data:
        raise HTTPException(status_code=400, detail="No data provided for update")
    
    update_data["updated_at"] = datetime.utcnow()
    
    # Update class in database
    await collection.update_one(
        {"_id": ObjectId(class_id)},
        {"$set": update_data}
    )
    
    # Return updated class
    updated_class = await collection.find_one({"_id": ObjectId(class_id)})
    return ClassInDB(**updated_class)


async def add_student_to_class(class_id: str, student_id: str) -> ClassResponse:
    """
    Add a student to class
    """
    collection = get_mongo_collection("classes")
    
    if not ObjectId.is_valid(class_id):
        raise HTTPException(status_code=400, detail="Invalid class ID format")
    
    # Check if class exists
    existing_class = await collection.find_one({"_id": ObjectId(class_id)})
    if not existing_class:
        raise HTTPException(status_code=404, detail="Class not found")
    
    # Add student to class if not already present
    if student_id not in existing_class.get("student_ids", []):
        await collection.update_one(
            {"_id": ObjectId(class_id)},
            {
                "$addToSet": {"student_ids": student_id},
                "$set": {"updated_at": datetime.utcnow()}
            }
        )
    
    # Return updated class
    updated_class = await collection.find_one({"_id": ObjectId(class_id)})
    return ClassInDB(**updated_class)


async def remove_student_from_class(class_id: str, student_id: str) -> ClassResponse:
    """
    Remove a student from class
    """
    collection = get_mongo_collection("classes")
    
    if not ObjectId.is_valid(class_id):
        raise HTTPException(status_code=400, detail="Invalid class ID format")
    
    # Check if class exists
    existing_class = await collection.find_one({"_id": ObjectId(class_id)})
    if not existing_class:
        raise HTTPException(status_code=404, detail="Class not found")
    
    # Remove student from class
    await collection.update_one(
        {"_id": ObjectId(class_id)},
        {
            "$pull": {"student_ids": student_id},
            "$set": {"updated_at": datetime.utcnow()}
        }
    )
    
    # Return updated class
    updated_class = await collection.find_one({"_id": ObjectId(class_id)})
    return ClassInDB(**updated_class)


async def delete_class(class_id: str) -> dict:
    """
    Delete class by ID
    """
    collection = get_mongo_collection("classes")
    
    if not ObjectId.is_valid(class_id):
        raise HTTPException(status_code=400, detail="Invalid class ID format")
    
    # Check if class exists
    existing_class = await collection.find_one({"_id": ObjectId(class_id)})
    if not existing_class:
        raise HTTPException(status_code=404, detail="Class not found")
    
    # Delete class
    result = await collection.delete_one({"_id": ObjectId(class_id)})
    
    if result.deleted_count == 1:
        return {"message": "Class deleted successfully"}
    else:
        raise HTTPException(status_code=500, detail="Failed to delete class")