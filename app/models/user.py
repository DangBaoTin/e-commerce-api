# app/models/user.py
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