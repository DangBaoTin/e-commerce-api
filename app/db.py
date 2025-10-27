# app/db.py
import os
from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv

# --- IMPORT YOUR MODELS HERE ---
from app.models import User  # <--- UPDATE THE IMPORT PATH

async def init_db():
    load_dotenv()
    db_url = os.getenv("DATABASE_URL")
    if not db_url:
        raise ValueError("DATABASE_URL not set in .env file")

    client = AsyncIOMotorClient(db_url)

    await init_beanie(
        database=client.get_default_database(), 
        document_models=[User]  # <--- (This stays the same)
    )
    
    print("Database connection initialized...")