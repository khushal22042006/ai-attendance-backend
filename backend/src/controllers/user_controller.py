from typing import List
from datetime import datetime
from bson import ObjectId
from fastapi import HTTPException
from models.user_model import UserCreate, UserResponse, UserUpdate, UserInDB
from config.db_connect import get_collection


async def create_user(user_data: UserCreate) -> UserResponse:
    """
    Create a new user in the database
    """
    collection = get_collection("users")
    
    # Check if user already exists
    existing_user = await collection.find_one({"email": user_data.email})
    if existing_user:
        raise HTTPException(status_code=400, detail="User with this email already exists")
    
    # Create user document
    user_doc = {
        "name": user_data.name,
        "email": user_data.email,
        "password": user_data.password,  # In real app, hash this password
        "role": user_data.role,
        "created_at": datetime.utcnow()
    }
    
    # Insert into database
    result = await collection.insert_one(user_doc)
    
    # Return created user
    created_user = await collection.find_one({"_id": result.inserted_id})
    return UserInDB(**created_user)


async def get_user(user_id: str) -> UserResponse:
    """
    Get user by ID
    """
    collection = get_collection("users")
    
    if not ObjectId.is_valid(user_id):
        raise HTTPException(status_code=400, detail="Invalid user ID format")
    
    user = await collection.find_one({"_id": ObjectId(user_id)})
    
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    return UserInDB(**user)


async def get_all_users() -> List[UserResponse]:
    """
    Get all users from database
    """
    collection = get_collection("users")
    
    users = []
    async for user in collection.find():
        users.append(UserInDB(**user))
    
    return users


async def update_user(user_id: str, user_data: UserUpdate) -> UserResponse:
    """
    Update user by ID
    """
    collection = get_collection("users")
    
    if not ObjectId.is_valid(user_id):
        raise HTTPException(status_code=400, detail="Invalid user ID format")
    
    # Check if user exists
    existing_user = await collection.find_one({"_id": ObjectId(user_id)})
    if not existing_user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Prepare update data (remove None values)
    update_data = {k: v for k, v in user_data.dict().items() if v is not None}
    
    if not update_data:
        raise HTTPException(status_code=400, detail="No data provided for update")
    
    # Update user in database
    await collection.update_one(
        {"_id": ObjectId(user_id)},
        {"$set": update_data}
    )
    
    # Return updated user
    updated_user = await collection.find_one({"_id": ObjectId(user_id)})
    return UserInDB(**updated_user)


async def delete_user(user_id: str) -> dict:
    """
    Delete user by ID
    """
    collection = get_collection("users")
    
    if not ObjectId.is_valid(user_id):
        raise HTTPException(status_code=400, detail="Invalid user ID format")
    
    # Check if user exists
    existing_user = await collection.find_one({"_id": ObjectId(user_id)})
    if not existing_user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Delete user
    result = await collection.delete_one({"_id": ObjectId(user_id)})
    
    if result.deleted_count == 1:
        return {"message": "User deleted successfully"}
    else:
        raise HTTPException(status_code=500, detail="Failed to delete user")
    