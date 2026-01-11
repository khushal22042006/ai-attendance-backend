from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel, Field, ConfigDict

# --- FIXED: Import from .base to avoid circular dependency ---
from .base import PyObjectId

class FaceEmbeddingCreate(BaseModel):
    student_id: str
    embedding: List[float]

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "student_id": "BCA2023_045",
                "embedding": [0.123, -0.345, 0.556]
            }
        }
    )

class FaceEmbeddingUpdate(BaseModel):
    embedding: List[float]

class FaceEmbeddingResponse(BaseModel):
    # Map MongoDB _id correctly using the PyObjectId type
    id: PyObjectId = Field(alias="_id")
    student_id: str
    embedding_length: int
    created_at: datetime

    model_config = ConfigDict(
        populate_by_name=True,
        from_attributes=True,
        json_schema_extra={
            "example": {
                "id": "65d5f8a9b4c7e12f34567894",
                "student_id": "BCA2023_045",
                "embedding_length": 128,
                "created_at": "2025-01-01T10:00:00"
            }
        }
    )

class FaceEmbeddingInDB(BaseModel):
    # ID is Optional so MongoDB can generate it on insert
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    student_id: str
    embedding: List[float]
    created_at: datetime = Field(default_factory=datetime.utcnow)

    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True
    )

class FaceMatchRequest(BaseModel):
    embedding: List[float]
    threshold: float = Field(0.6, ge=0.0, le=1.0) # Adjusted default for face matching

class FaceMatchResponse(BaseModel):
    matched: bool
    student_id: Optional[str] = None
    confidence: Optional[float] = None
    message: str