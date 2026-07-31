from typing import Optional
from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field
from beanie import PydanticObjectId


class ItemCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = None
    price: float = Field(default=0.0, ge=0.0)
    is_available: bool = True


class ItemUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str] = None
    price: Optional[float] = Field(None, ge=0.0)
    is_available: Optional[bool] = None


class ItemResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: PydanticObjectId
    title: str
    description: Optional[str] = None
    price: float
    is_available: bool
    created_at: datetime
