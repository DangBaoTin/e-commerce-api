# app/schemas/cart.py
from pydantic import BaseModel, Field
from beanie import PydanticObjectId
from typing import List

class CartItemCreate(BaseModel):
    product_id: PydanticObjectId
    quantity: int = Field(..., gt=0)

class CartItemOut(BaseModel):
    product_id: PydanticObjectId
    quantity: int
    class Config:
        from_attributes = True

class CartOut(BaseModel):
    id: str
    user_id: PydanticObjectId
    items: List[CartItemOut]
    class Config:
        from_attributes = True
        json_encoders = {"id": str}