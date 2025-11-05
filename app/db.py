from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient
from app.core.config import settings

from app.models.user import User
from app.models.product import Product
from app.models.cart import Cart
from app.models.order import Order

async def init_db():
    db_url = settings.DATABASE_URL
    if not db_url:
        raise ValueError("DATABASE_URL not set")

    client = AsyncIOMotorClient(db_url)

    await init_beanie(
        database=client.get_default_database(), # pyright: ignore[reportArgumentType]
        document_models=[User, Product, Cart, Order]
    )
    
    print("Database connection initialized...")