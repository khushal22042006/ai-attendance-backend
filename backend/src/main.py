import uvicorn
import sys
import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware
from contextlib import asynccontextmanager

# 1. Path Setup
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# 2. Imports
from routes import auth_routes
from config.db_connect import init_mongodb, close_mongodb, get_mongodb_status

# 3. Lifespan Manager
@asynccontextmanager
async def lifespan(app: FastAPI):
    print("🚀 Starting AI Attendance Backend...")
    try:
        await init_mongodb()
        print("✅ MongoDB Connection Initialized")
    except Exception as e:
        print(f"❌ MongoDB initialization failed: {e}")
        print("ℹ️ API running in limited mode.")
    
    yield
    
    print("🛑 Shutting down...")
    await close_mongodb()

# 4. App Instance
app = FastAPI(
    title="AI Attendance Backend",
    description="Intelligent attendance tracking system",
    version="1.0.0",
    lifespan=lifespan
)

# 5. Middleware (ORDER IS CRITICAL FOR OAUTH)

# SESSION_SECRET must be loaded before middleware definition
# Pulling from .env ensures it matches the state saved during redirect
SESSION_SECRET = os.getenv("SECRET_KEY")

# SessionMiddleware MUST be added BEFORE CORSMiddleware for Starlette/FastAPI 
# to correctly handle CSRF state cookies during redirects.
app.add_middleware(
    SessionMiddleware, 
    secret_key=SESSION_SECRET,
    same_site="lax",    # Allows cookies to be sent back after Google redirect
    https_only=False    # Set to False for local 127.0.0.1 development
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True, # Required for session cookies to work
    allow_methods=["*"],
    allow_headers=["*"],
)

# 6. Include Routers
app.include_router(auth_routes.router)

# 7. Endpoints
@app.get("/")
def root():
    return {
        "message": "AI Attendance Backend API",
        "status": "online",
        "docs": "/docs"
    }

@app.get("/health")
async def health_check():
    db_status = await get_mongodb_status()
    return {
        "status": "healthy" if db_status.get("connected") else "degraded",
        "database": db_status
    }

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)