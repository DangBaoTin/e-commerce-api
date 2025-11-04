# app/db.py
import os
from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient
from app.core.config import settings

from app.models import User, Product, Cart

async def init_db():
    db_url = settings.DATABASE_URL
    if not db_url:
        raise ValueError("DATABASE_URL not set in .env file")

    client = AsyncIOMotorClient(db_url)

    await init_beanie(
        database=client.get_default_database(),  # type: ignore
        document_models=[User, Product, Cart]
    )
    
    print("Database connection initialized...")