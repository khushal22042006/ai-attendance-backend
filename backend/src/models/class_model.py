from typing import Optional, List
from datetime import datetime
from pydantic import BaseModel, Field, ConfigDict

# Import the shared type to maintain consistency across the app
from .base import PyObjectId

class ClassCreate(BaseModel):
    class_name: str = Field(..., min_length=2, max_length=100)
    section: str = Field(..., min_length=1, max_length=5)
    subjects: List[str] = Field(..., min_length=1) # Pydantic v2 uses min_length for lists

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
    # Map MongoDB's _id to id in the JSON response
    id: PyObjectId = Field(alias="_id")
    class_name: str
    section: str
    subjects: List[str]
    created_at: datetime

    model_config = ConfigDict(
        populate_by_name=True,
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
    # Let MongoDB handle ID generation by making it Optional in the model
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    class_name: str
    section: str
    subjects: List[str]
    created_at: datetime = Field(default_factory=datetime.utcnow)

    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True
    )