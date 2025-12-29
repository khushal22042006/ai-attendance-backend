from typing import List, Optional
from datetime import datetime
from bson import ObjectId
from pydantic import BaseModel, Field, ConfigDict
from .user_model import PyObjectId


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
    id: str
    student_id: str
    embedding_length: int
    created_at: datetime

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "id": "65d5f8a9b4c7e12f34567894",
                "student_id": "BCA2023_045",
                "embedding_length": 3,
                "created_at": "2025-01-01T10:00:00"
            }
        }
    )


class FaceEmbeddingInDB(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    student_id: str
    embedding: List[float]
    created_at: datetime = Field(default_factory=datetime.utcnow)

    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
        json_schema_extra={
            "example": {
                "_id": "65d5f8a9b4c7e12f34567894",
                "student_id": "BCA2023_045",
                "embedding": [0.123, -0.345, 0.556],
                "created_at": "2025-01-01T10:00:00"
            }
        }
    )


class FaceMatchRequest(BaseModel):
    embedding: List[float]
    threshold: float = Field(0.7, ge=0.0, le=1.0)


class FaceMatchResponse(BaseModel):
    matched: bool
    student_id: Optional[str] = None
    confidence: Optional[float] = None
    message: str