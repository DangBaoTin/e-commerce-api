from beanie import Document

class Product(Document):
    name: str
    description: str
    price: float
    stock: int = 0

    class Settings:
        name = "products"