from contextlib import asynccontextmanager
from typing import List
from fastapi import FastAPI, HTTPException, status
from beanie import PydanticObjectId

from db import init_db
from models import Item
from schemas import ItemCreate, ItemResponse, ItemUpdate


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Initialize database connection on startup
    await init_db()
    yield


app = FastAPI(title="Beanie CRUD Service for CI/CD Testing", lifespan=lifespan)


@app.get("/health", status_code=status.HTTP_200_OK)
async def health_check():
    return {"status": "healthy", "service": "beanie-crud-api"}


@app.post("/items/", response_model=ItemResponse, status_code=status.HTTP_201_CREATED)
async def create_item(item_in: ItemCreate):
    item = Item(**item_in.model_dump())
    await item.insert()
    return item


@app.get("/items/", response_model=List[ItemResponse])
async def get_items(limit: int = 10, skip: int = 0):
    return await Item.find_all().skip(skip).limit(limit).to_list()


@app.get("/items/{item_id}", response_model=ItemResponse)
async def get_item(item_id: PydanticObjectId):
    item = await Item.get(item_id)
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Item with id '{item_id}' not found",
        )
    return item


@app.put("/items/{item_id}", response_model=ItemResponse)
async def update_item(item_id: PydanticObjectId, item_in: ItemUpdate):
    item = await Item.get(item_id)
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Item with id '{item_id}' not found",
        )

    update_data = item_in.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(item, key, value)

    await item.save()
    return item


@app.delete("/items/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_item(item_id: PydanticObjectId):
    item = await Item.get(item_id)
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Item with id '{item_id}' not found",
        )
    await item.delete()
    return None
