# backend/src/routes/face_embedding_routes.py
from typing import List
from fastapi import APIRouter, HTTPException
from models.face_embeding_model import (
    FaceEmbeddingCreate, 
    FaceEmbeddingResponse, 
    FaceEmbeddingUpdate
)
from controllers.face_embedding_controller import (
    create_face_embedding,
    get_face_embedding,
    get_face_embedding_by_student,
    get_all_face_embeddings,
    get_active_face_embeddings,
    update_face_embedding,
    deactivate_face_embedding,
    reactivate_face_embedding,
    delete_face_embedding,
    find_similar_faces
)

router = APIRouter()

@router.post("/", response_model=FaceEmbeddingResponse)
async def create_face_embedding_route(embedding_data: FaceEmbeddingCreate):
    """Create a new face embedding"""
    return await create_face_embedding(embedding_data)

@router.get("/{embedding_id}", response_model=FaceEmbeddingResponse)
async def get_face_embedding_route(embedding_id: str):
    """Get face embedding by ID"""
    return await get_face_embedding(embedding_id)

@router.get("/student/{student_id}", response_model=FaceEmbeddingResponse)
async def get_face_embedding_by_student_route(student_id: str):
    """Get face embedding by student ID"""
    return await get_face_embedding_by_student(student_id)

@router.get("/", response_model=list[FaceEmbeddingResponse])
async def get_all_face_embeddings_route():
    """Get all face embeddings"""
    return await get_all_face_embeddings()

@router.get("/active/all", response_model=list[FaceEmbeddingResponse])
async def get_active_face_embeddings_route():
    """Get all active face embeddings"""
    return await get_active_face_embeddings()

@router.put("/{embedding_id}", response_model=FaceEmbeddingResponse)
async def update_face_embedding_route(embedding_id: str, embedding_data: FaceEmbeddingUpdate):
    """Update face embedding by ID"""
    return await update_face_embedding(embedding_id, embedding_data)

@router.post("/{embedding_id}/deactivate", response_model=FaceEmbeddingResponse)
async def deactivate_face_embedding_route(embedding_id: str):
    """Deactivate a face embedding"""
    return await deactivate_face_embedding(embedding_id)

@router.post("/{embedding_id}/reactivate", response_model=FaceEmbeddingResponse)
async def reactivate_face_embedding_route(embedding_id: str):
    """Reactivate a face embedding"""
    return await reactivate_face_embedding(embedding_id)

@router.delete("/{embedding_id}")
async def delete_face_embedding_route(embedding_id: str):
    """Delete face embedding by ID"""
    return await delete_face_embedding(embedding_id)

@router.post("/similarity/find")
async def find_similar_faces_route(embedding: List[float], threshold: float = 0.7, limit: int = 10):
    """Find faces similar to the provided embedding"""
    return await find_similar_faces(embedding, threshold, limit)