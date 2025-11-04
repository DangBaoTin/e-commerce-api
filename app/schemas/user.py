# app/schemas/user.py
from pydantic import BaseModel, EmailStr, Field

class UserCreate(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    password: str = Field(..., min_length=8, max_length=71)

class UserOut(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    is_admin: bool