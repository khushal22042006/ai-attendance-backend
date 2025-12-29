# backend/src/main_working.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import uvicorn
import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifespan context manager for startup/shutdown events
    """
    # Startup
    print("🚀 Starting AI Attendance Backend...")
    
    # Initialize MongoDB (optional - will work even if MongoDB is not available)
    try:
        from config.db_connect import init_mongodb
        await init_mongodb()
    except Exception as e:
        print(f"ℹ️ MongoDB initialization skipped or failed: {e}")
        print("ℹ️ API will still work for basic endpoints")
    
    yield
    
    # Shutdown
    print("🛑 Shutting down...")
    try:
        from config.db_connect import close_mongodb
        await close_mongodb()
    except:
        pass


# Create FastAPI app
app = FastAPI(
    title="AI Attendance Backend",
    description="Intelligent attendance tracking system",
    version="1.0.0",
    lifespan=lifespan
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Import and include routes - simplified version
try:
    from fastapi import APIRouter, HTTPException
    from pydantic import BaseModel
    from datetime import datetime
    from typing import List, Optional
    import uuid
    
    # Simple user model without EmailStr validation for now
    class UserCreate(BaseModel):
        name: str
        email: str  # We'll add email validation later
        password: str
        role: str = "student"
    
    class UserResponse(BaseModel):
        id: str
        name: str
        email: str
        role: str
        created_at: datetime
    
    # Create router
    user_router = APIRouter()
    
    # In-memory storage for testing
    users_store = []
    
    @user_router.post("/", response_model=UserResponse)
    async def create_user(user: UserCreate):
        """Create a new user"""
        # Simple email validation
        if "@" not in user.email or "." not in user.email:
            raise HTTPException(status_code=400, detail="Invalid email format")
        
        # Check if user already exists
        if any(u["email"] == user.email for u in users_store):
            raise HTTPException(status_code=400, detail="User with this email already exists")
        
        user_data = {
            "id": str(uuid.uuid4()),
            "name": user.name,
            "email": user.email,
            "password": user.password,  # In production, hash this!
            "role": user.role,
            "created_at": datetime.utcnow()
        }
        users_store.append(user_data)
        return user_data
    
    @user_router.get("/", response_model=List[UserResponse])
    async def get_users():
        """Get all users"""
        return users_store
    
    @user_router.get("/{user_id}", response_model=UserResponse)
    async def get_user(user_id: str):
        """Get user by ID"""
        for user in users_store:
            if user["id"] == user_id:
                return user
        raise HTTPException(status_code=404, detail="User not found")
    
    # Include the router
    app.include_router(user_router, prefix="/api/users", tags=["Users"])
    print("✅ User routes loaded (in-memory storage)")
    
except Exception as e:
    print(f"⚠️ Error creating user routes: {e}")

# Root endpoint
@app.get("/")
def root():
    return {
        "message": "AI Attendance Backend API",
        "version": "1.0.0",
        "docs": "/docs",
        "redoc": "/redoc",
        "endpoints": {
            "users": "/api/users",
            "health": "/health"
        }
    }


# Health check endpoint
@app.get("/health")
async def health_check():
    """
    Health check for load balancers and monitoring
    """
    try:
        from config.db_connect import get_mongodb_status
        db_status = await get_mongodb_status()
        return {
            "status": "healthy" if db_status.get("connected") else "degraded",
            "service": "ai-attendance-backend",
            "version": "1.0.0",
            "database": db_status
        }
    except Exception as e:
        return {
            "status": "healthy",
            "service": "ai-attendance-backend",
            "version": "1.0.0",
            "database": "not_configured",
            "note": "Using in-memory storage"
        }


# Run server
if __name__ == "__main__":
    uvicorn.run(
        "main_working:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )