from typing import List
from datetime import datetime
from bson import ObjectId
from pydantic import BaseModel, Field, ConfigDict
from .user_model import PyObjectId


class ClassCreate(BaseModel):
    class_name: str = Field(..., min_length=2, max_length=100)
    section: str = Field(..., min_length=1, max_length=5)
    subjects: List[str] = Field(..., min_items=1)

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "class_name": "BCA 2nd Year",
                "section": "A",
                "subjects": ["AI", "DBMS", "OS"]
            }
        }
    )


class ClassUpdate(BaseModel):
    class_name: Optional[str] = Field(None, min_length=2, max_length=100)
    section: Optional[str] = Field(None, min_length=1, max_length=5)
    subjects: Optional[List[str]] = None


class ClassResponse(BaseModel):
    id: str
    class_name: str
    section: str
    subjects: List[str]
    created_at: datetime

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "id": "65d5f8a9b4c7e12f34567892",
                "class_name": "BCA 2nd Year",
                "section": "A",
                "subjects": ["AI", "DBMS", "OS"],
                "created_at": "2024-12-01T09:00:00"
            }
        }
    )


class ClassInDB(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    class_name: str
    section: str
    subjects: List[str]
    created_at: datetime = Field(default_factory=datetime.utcnow)

    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
        json_schema_extra={
            "example": {
                "_id": "65d5f8a9b4c7e12f34567892",
                "class_name": "BCA 2nd Year",
                "section": "A",
                "subjects": ["AI", "DBMS", "OS"],
                "created_at": "2024-12-01T09:00:00"
            }
        }
    )