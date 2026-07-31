from typing import Optional
from datetime import datetime, timezone
from beanie import Document
from pydantic import Field


class Item(Document):
    title: str
    description: Optional[str] = None
    price: float = 0.0
    is_available: bool = True
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    class Settings:
        name = "items"
