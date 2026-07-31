from datetime import datetime

from beanie import PydanticObjectId
from pydantic import BaseModel, ConfigDict, Field


class ItemCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=100)
    description: str | None = None
    price: float = Field(default=0.0, ge=0.0)
    is_available: bool = True


class ItemUpdate(BaseModel):
    title: str | None = Field(None, min_length=1, max_length=100)
    description: str | None = None
    price: float | None = Field(None, ge=0.0)
    is_available: bool | None = None


class ItemResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: PydanticObjectId
    title: str
    description: str | None = None
    price: float
    is_available: bool
    created_at: datetime
