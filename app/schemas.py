from pydantic import BaseModel, EmailStr
from typing import Optional

class UserCreate(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    password: str

class UserOut(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    is_admin: bool

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None

class ProductCreate(BaseModel):
    """
    Pydantic model for creating a new product.
    """
    name: str
    description: str
    price: float
    stock: int = 0

class ProductOut(BaseModel):
    """
    Pydantic model for sending product data to the client.
    """
    id: str  # We'll send the MongoDB ID as a string
    name: str
    description: str
    price: float
    stock: int
    
    class Config:
        # This tells Pydantic to get the 'id' from the model's '_id' attribute
        from_attributes = True 
        # In Pydantic v1, this was `orm_mode = True`
        # We also need to tell it how to handle Beanie's ObjectId
        json_encoders = {
            "id": str  # This is a fallback, but from_attributes is key
        }

class ProductUpdate(BaseModel):
    """
    Pydantic model for updating an existing product.
    All fields are optional.
    """
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    stock: Optional[int] = None