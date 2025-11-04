# app/models/cart.py
from beanie import Document, PydanticObjectId
from pydantic import BaseModel
from typing import List

class CartItem(BaseModel):
    product_id: PydanticObjectId
    quantity: int

class Cart(Document):
    user_id: PydanticObjectId
    items: List[CartItem] = []

    class Settings:
        name = "carts"