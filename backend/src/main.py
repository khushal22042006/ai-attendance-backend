from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import uvicorn
import sys
import os

# Add src to path for imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifespan context manager for startup/shutdown events
    """
    # Startup
    print(" Starting AI Attendance Backend...")
    
    # Initialize MongoDB
    try:
        from config.db_connect import init_mongodb
        await init_mongodb()
    except ImportError as e:
        print(f"⚠️ MongoDB initialization skipped: {e}")
        print("ℹ️ Install: poetry add motor pymongo")
    except Exception as e:
        print(f"⚠️ MongoDB connection error: {e}")
    
    # Initialize PostgreSQL (if needed in future)
    # try:
    #     from config.database import init_postgresql
    #     await init_postgresql()
    # except Exception as e:
    #     print(f"⚠️ PostgreSQL initialization skipped: {e}")
    
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

# Import and include routes
try:
    from routes import user_routes
    app.include_router(
        user_routes.router,
        prefix="/api/users",
        tags=["Users"]
    )
    print("✅ User routes loaded")
except ImportError as e:
    print(f"⚠️ User routes not loaded: {e}")

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
    from config.db_connect import get_mongodb_status
    
    db_status = await get_mongodb_status()
    
    return {
        "status": "healthy" if db_status["connected"] else "degraded",
        "service": "ai-attendance-backend",
        "version": "1.0.0",
        "database": db_status
    }


# Run server
if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )