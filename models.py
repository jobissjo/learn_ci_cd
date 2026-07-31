from datetime import UTC, datetime

from beanie import Document
from pydantic import Field


class Item(Document):
    title: str
    description: str | None = None
    price: float = 0.0
    is_available: bool = True
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))

    class Settings:
        name = "items"
