# backend/src/config/db_connect.py (fixed)
import os
from typing import Optional
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# MongoDB Configuration
MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
MONGO_DB_NAME = os.getenv("DB_NAME", "ai_attendance")

# Global MongoDB client
mongo_client = None
mongo_db = None


async def init_mongodb():
    """
    Initialize MongoDB connection
    """
    global mongo_client, mongo_db
    
    try:
        # Import motor
        from motor.motor_asyncio import AsyncIOMotorClient
        from pymongo.errors import ConnectionFailure, ServerSelectionTimeoutError
        
        print(f"🔗 Connecting to MongoDB at {MONGO_DB_NAME}")
        
        # Create async client
        mongo_client = AsyncIOMotorClient(
            MONGO_URI,
            maxPoolSize=50,
            minPoolSize=10,
            serverSelectionTimeoutMS=5000,
            connectTimeoutMS=10000,
            socketTimeoutMS=30000
        )
        
        # Test connection
        await mongo_client.admin.command('ping')
        
        # Get database
        mongo_db = mongo_client[MONGO_DB_NAME]
        
        print(f"✅ MongoDB connected: {MONGO_DB_NAME}")
        
        # Create indexes
        await create_mongo_indexes()
        
    except ImportError:
        print("❌ 'motor' package not found. Install with: poetry add motor")
        raise
    except (ConnectionFailure, ServerSelectionTimeoutError) as e:
        print(f"❌ MongoDB connection failed: {e}")
        print("ℹ️  Make sure MongoDB is running: docker run -d -p 27017:27017 mongo")
        raise
    except Exception as e:
        print(f"⚠️  MongoDB error: {e}")
        raise


async def create_mongo_indexes():
    """
    Create necessary indexes in MongoDB
    """
    try:
        if mongo_db is None:
            print("⚠️  MongoDB database not initialized")
            return
            
        # Create indexes for users collection
        await mongo_db.users.create_index("email", unique=True)
        await mongo_db.users.create_index("role")
        await mongo_db.users.create_index("created_at")
        
        print("✅ MongoDB indexes created")
    except Exception as e:
        print(f"⚠️  Could not create indexes: {e}")


async def get_mongodb_status() -> dict:
    """
    Get MongoDB connection status
    """
    if mongo_client is None:
        return {"connected": False, "error": "Not initialized"}
    
    try:
        await mongo_client.admin.command('ping')
        return {
            "connected": True,
            "database": MONGO_DB_NAME,
            "collections": await mongo_db.list_collection_names()
        }
    except Exception as e:
        return {"connected": False, "error": str(e)}


async def close_mongodb():
    """
    Close MongoDB connection
    """
    global mongo_client
    if mongo_client:
        mongo_client.close()
        print("✅ MongoDB connection closed")


def get_mongo_database():
    """
    Get MongoDB database instance
    """
    if mongo_db is None:
        raise Exception("MongoDB not initialized. Call init_mongodb() first.")
    return mongo_db


def get_mongo_collection(collection_name: str):
    """
    Get MongoDB collection
    """
    db = get_mongo_database()
    return db[collection_name]


# For dependency injection
async def get_db():
    """
    Dependency for FastAPI routes
    """
    yield mongo_db

# This allows 'from config.db_connect import user_collection' to work
def user_collection():
    return get_mongo_collection("users")

# Note: We keep the variable export simple so your dependencies can find it
from motor.motor_asyncio import AsyncIOMotorClient
# We provide a property-like access if you want to keep the existing dependency style
@property
def user_collection_ptr():
    return get_mongo_collection("users")