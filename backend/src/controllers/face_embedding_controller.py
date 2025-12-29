# backend/src/controllers/face_embedding_controller.py
from typing import List
from datetime import datetime
from bson import ObjectId
import numpy as np
from fastapi import HTTPException
from models.face_embedding_model import (
    FaceEmbeddingCreate, 
    FaceEmbeddingResponse, 
    FaceEmbeddingUpdate, 
    FaceEmbeddingInDB
)
from config.db_connect import get_mongo_collection


async def create_face_embedding(embedding_data: FaceEmbeddingCreate) -> FaceEmbeddingResponse:
    """
    Create a new face embedding
    """
    collection = get_mongo_collection("face_embeddings")
    
    # Check if embedding already exists for this student
    existing_embedding = await collection.find_one({"student_id": embedding_data.student_id})
    if existing_embedding:
        raise HTTPException(status_code=400, detail="Face embedding already exists for this student")
    
    # Convert embedding list to numpy array and back to list for storage
    if isinstance(embedding_data.embedding, list):
        embedding_array = np.array(embedding_data.embedding, dtype=np.float32)
    else:
        embedding_array = embedding_data.embedding
    
    # Create embedding document
    embedding_doc = {
        "student_id": embedding_data.student_id,
        "embedding": embedding_array.tolist(),  # Store as list
        "embedding_version": embedding_data.embedding_version,
        "model_used": embedding_data.model_used,
        "image_paths": embedding_data.image_paths or [],
        "metadata": embedding_data.metadata or {},
        "is_active": embedding_data.is_active,
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow()
    }
    
    # Insert into database
    result = await collection.insert_one(embedding_doc)
    
    # Return created embedding
    created_embedding = await collection.find_one({"_id": result.inserted_id})
    return FaceEmbeddingInDB(**created_embedding)


async def get_face_embedding(embedding_id: str) -> FaceEmbeddingResponse:
    """
    Get face embedding by ID
    """
    collection = get_mongo_collection("face_embeddings")
    
    if not ObjectId.is_valid(embedding_id):
        raise HTTPException(status_code=400, detail="Invalid embedding ID format")
    
    embedding = await collection.find_one({"_id": ObjectId(embedding_id)})
    
    if not embedding:
        raise HTTPException(status_code=404, detail="Face embedding not found")
    
    return FaceEmbeddingInDB(**embedding)


async def get_face_embedding_by_student(student_id: str) -> FaceEmbeddingResponse:
    """
    Get face embedding by student ID
    """
    collection = get_mongo_collection("face_embeddings")
    
    embedding = await collection.find_one({"student_id": student_id})
    
    if not embedding:
        raise HTTPException(status_code=404, detail="Face embedding not found for this student")
    
    return FaceEmbeddingInDB(**embedding)


async def get_all_face_embeddings() -> List[FaceEmbeddingResponse]:
    """
    Get all face embeddings
    """
    collection = get_mongo_collection("face_embeddings")
    
    embeddings = []
    async for embedding in collection.find():
        embeddings.append(FaceEmbeddingInDB(**embedding))
    
    return embeddings


async def get_active_face_embeddings() -> List[FaceEmbeddingResponse]:
    """
    Get all active face embeddings
    """
    collection = get_mongo_collection("face_embeddings")
    
    embeddings = []
    async for embedding in collection.find({"is_active": True}):
        embeddings.append(FaceEmbeddingInDB(**embedding))
    
    return embeddings


async def update_face_embedding(embedding_id: str, embedding_data: FaceEmbeddingUpdate) -> FaceEmbeddingResponse:
    """
    Update face embedding by ID
    """
    collection = get_mongo_collection("face_embeddings")
    
    if not ObjectId.is_valid(embedding_id):
        raise HTTPException(status_code=400, detail="Invalid embedding ID format")
    
    # Check if embedding exists
    existing_embedding = await collection.find_one({"_id": ObjectId(embedding_id)})
    if not existing_embedding:
        raise HTTPException(status_code=404, detail="Face embedding not found")
    
    # Prepare update data
    update_data = {k: v for k, v in embedding_data.dict().items() if v is not None}
    
    # Handle embedding conversion
    if "embedding" in update_data and update_data["embedding"] is not None:
        if isinstance(update_data["embedding"], list):
            embedding_array = np.array(update_data["embedding"], dtype=np.float32)
        else:
            embedding_array = update_data["embedding"]
        update_data["embedding"] = embedding_array.tolist()
    
    if not update_data:
        raise HTTPException(status_code=400, detail="No data provided for update")
    
    update_data["updated_at"] = datetime.utcnow()
    
    # Update embedding in database
    await collection.update_one(
        {"_id": ObjectId(embedding_id)},
        {"$set": update_data}
    )
    
    # Return updated embedding
    updated_embedding = await collection.find_one({"_id": ObjectId(embedding_id)})
    return FaceEmbeddingInDB(**updated_embedding)


async def deactivate_face_embedding(embedding_id: str) -> FaceEmbeddingResponse:
    """
    Deactivate a face embedding
    """
    collection = get_mongo_collection("face_embeddings")
    
    if not ObjectId.is_valid(embedding_id):
        raise HTTPException(status_code=400, detail="Invalid embedding ID format")
    
    # Check if embedding exists
    existing_embedding = await collection.find_one({"_id": ObjectId(embedding_id)})
    if not existing_embedding:
        raise HTTPException(status_code=404, detail="Face embedding not found")
    
    # Deactivate embedding
    await collection.update_one(
        {"_id": ObjectId(embedding_id)},
        {
            "$set": {
                "is_active": False,
                "updated_at": datetime.utcnow()
            }
        }
    )
    
    # Return updated embedding
    updated_embedding = await collection.find_one({"_id": ObjectId(embedding_id)})
    return FaceEmbeddingInDB(**updated_embedding)


async def reactivate_face_embedding(embedding_id: str) -> FaceEmbeddingResponse:
    """
    Reactivate a face embedding
    """
    collection = get_mongo_collection("face_embeddings")
    
    if not ObjectId.is_valid(embedding_id):
        raise HTTPException(status_code=400, detail="Invalid embedding ID format")
    
    # Check if embedding exists
    existing_embedding = await collection.find_one({"_id": ObjectId(embedding_id)})
    if not existing_embedding:
        raise HTTPException(status_code=404, detail="Face embedding not found")
    
    # Reactivate embedding
    await collection.update_one(
        {"_id": ObjectId(embedding_id)},
        {
            "$set": {
                "is_active": True,
                "updated_at": datetime.utcnow()
            }
        }
    )
    
    # Return updated embedding
    updated_embedding = await collection.find_one({"_id": ObjectId(embedding_id)})
    return FaceEmbeddingInDB(**updated_embedding)


async def delete_face_embedding(embedding_id: str) -> dict:
    """
    Delete face embedding by ID
    """
    collection = get_mongo_collection("face_embeddings")
    
    if not ObjectId.is_valid(embedding_id):
        raise HTTPException(status_code=400, detail="Invalid embedding ID format")
    
    # Check if embedding exists
    existing_embedding = await collection.find_one({"_id": ObjectId(embedding_id)})
    if not existing_embedding:
        raise HTTPException(status_code=404, detail="Face embedding not found")
    
    # Delete embedding
    result = await collection.delete_one({"_id": ObjectId(embedding_id)})
    
    if result.deleted_count == 1:
        return {"message": "Face embedding deleted successfully"}
    else:
        raise HTTPException(status_code=500, detail="Failed to delete face embedding")


async def find_similar_faces(embedding: List[float], threshold: float = 0.7, limit: int = 10) -> List[dict]:
    """
    Find faces similar to the provided embedding
    This is a simplified version - in production, you'd use a vector database
    """
    collection = get_mongo_collection("face_embeddings")
    
    query_embedding = np.array(embedding, dtype=np.float32)
    
    similar_faces = []
    
    # Get all active embeddings
    async for face_embedding in collection.find({"is_active": True}):
        db_embedding = np.array(face_embedding["embedding"], dtype=np.float32)
        
        # Calculate cosine similarity
        similarity = np.dot(query_embedding, db_embedding) / (
            np.linalg.norm(query_embedding) * np.linalg.norm(db_embedding)
        )
        
        if similarity >= threshold:
            similar_faces.append({
                "student_id": face_embedding["student_id"],
                "similarity": float(similarity),
                "embedding_id": str(face_embedding["_id"])
            })
    
    # Sort by similarity
    similar_faces.sort(key=lambda x: x["similarity"], reverse=True)
    
    return similar_faces[:limit]