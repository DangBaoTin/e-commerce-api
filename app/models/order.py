from beanie import Document, PydanticObjectId
from pydantic import BaseModel, Field
from typing import List
from datetime import datetime

class OrderItem(BaseModel):
    product_id: PydanticObjectId
    quantity: int
    price_at_purchase: float

class Order(Document):
    user_id: PydanticObjectId
    items: List[OrderItem]
    total_price: float
    order_status: str = "pending"
    created_at: datetime = Field(default_factory=datetime.now)

    class Settings:
        name = "orders"