from pydantic import BaseModel, HttpUrl
from beanie import PydanticObjectId
from typing import List
from datetime import datetime

class OrderItemOut(BaseModel):
    product_id: PydanticObjectId
    quantity: int
    price_at_purchase: float
    class Config:
        from_attributes = True

class OrderOut(BaseModel):
    id: str
    user_id: PydanticObjectId
    items: List[OrderItemOut]
    total_price: float
    order_status: str
    created_at: datetime
    class Config:
        from_attributes = True
        json_encoders = {"id": str}

class CheckoutSessionResponse(BaseModel):
    """
    Pydantic model for sending the Stripe Checkout session URL.
    """
    url: HttpUrl