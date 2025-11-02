from beanie import Document, PydanticObjectId
from pydantic import BaseModel, EmailStr
from typing import List

class CartItem(BaseModel):
    """
    Represents an item within a cart.
    This is an embedded Pydantic model, not a Beanie Document.
    """
    product_id: PydanticObjectId
    quantity: int

class User(Document):
    first_name: str
    last_name: str
    email: EmailStr
    hashed_password: str
    is_admin: bool = False

    class Settings:
        name = "users"

class Product(Document):
    """
    Represents a Product in the database.
    """
    name: str
    description: str
    price: float
    stock: int = 0

    class Settings:
        name = "products"

class Cart(Document):
    """
    Represents a User's shopping cart.
    """
    user_id: PydanticObjectId  # Link to the User
    items: List[CartItem] = [] # A list of embedded CartItem models

    class Settings:
        name = "carts"