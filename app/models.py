from beanie import Document
from pydantic import EmailStr

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