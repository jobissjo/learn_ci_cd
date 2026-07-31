import os

from beanie import init_beanie
from dotenv import load_dotenv
from pymongo import AsyncMongoClient

from models import Item

load_dotenv()

MONGODB_URL = os.getenv("MONGODB_URL", "mongodb://localhost:27017")


async def init_db():
    client = AsyncMongoClient(MONGODB_URL)
    await init_beanie(database=client.get_database(), document_models=[Item])
