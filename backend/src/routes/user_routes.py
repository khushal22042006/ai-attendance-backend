from fastapi import APIRouter, HTTPException, Depends
from models.user_model import UserCreate, UserResponse, UserUpdate
from controllers.user_controller import (
    create_user,
    get_user,
    get_all_users,
    update_user,
    delete_user
)

router = APIRouter()

@router.post("/", response_model=UserResponse)
async def create_user_route(user_data: UserCreate):
    """Create a new user"""
    return await create_user(user_data)

@router.get("/{user_id}", response_model=UserResponse)
async def get_user_route(user_id: str):
    """Get user by ID"""
    return await get_user(user_id)

@router.get("/", response_model=list[UserResponse])
async def get_users_route():
    """Get all users"""
    return await get_all_users()

@router.put("/{user_id}", response_model=UserResponse)
async def update_user_route(user_id: str, user_data: UserUpdate):
    """Update user by ID"""
    return await update_user(user_id, user_data)

@router.delete("/{user_id}")
async def delete_user_route(user_id: str):
    """Delete user by ID"""
    return await delete_user(user_id)