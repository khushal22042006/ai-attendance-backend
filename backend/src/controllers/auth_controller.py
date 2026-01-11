from fastapi import HTTPException, status
from models.user_model import UserCreate, UserLoginRequest
from utils.security import get_password_hash, verify_password, create_access_token
from config.db_connect import get_mongo_collection # Import your utility
from datetime import datetime

# Helper to get the collection
def get_users_collection():
    return get_mongo_collection("users")

async def register_user(user: UserCreate):
    collection = get_users_collection()
    
    # Check if user exists in MongoDB
    existing_user = await collection.find_one({"email": user.email})
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    hashed_password = get_password_hash(user.password)
    
    # Prepare document for MongoDB
    new_user = {
        "name": user.name,
        "email": user.email,
        "hashed_password": hashed_password,
        "role": user.role,
        "created_at": datetime.now() # Best to track when they joined
    }
    
    await collection.insert_one(new_user)
    return {"message": "User created successfully"}

async def login_user(login_data: UserLoginRequest):
    collection = get_users_collection()
    
    # Find user by email (stored in login_data.username)
    user = await collection.find_one({"email": login_data.username})
    
    # Check if user exists and password is correct
    if not user or not verify_password(login_data.password, user.get("hashed_password", "")):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token = create_access_token(data={"sub": user["email"]})
    return {"access_token": access_token, "token_type": "bearer"}

async def handle_google_login(user_info):
    collection = get_users_collection()
    email = user_info.get("email")
    
    # Upsert logic: Find user or create if they don't exist
    user = await collection.find_one({"email": email})
    
    if not user:
        new_user = {
            "email": email,
            "name": user_info.get("name"),
            "google_id": user_info.get("sub"),
            "role": "student", # Default role
            "created_at": datetime.now()
        }
        await collection.insert_one(new_user)
        
    access_token = create_access_token(data={"sub": email})
    return {"access_token": access_token, "token_type": "bearer"}