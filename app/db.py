# app/db.py
import os
from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv

from app.models import User

async def init_db():
    load_dotenv()
    db_url = os.getenv("DATABASE_URL")
    if not db_url:
        raise ValueError("DATABASE_URL not set in .env file")

    client = AsyncIOMotorClient(db_url)

    await init_beanie(
        database=client.get_default_database(),  # type: ignore
        document_models=[User]
    )
    
    print("Database connection initialized...")