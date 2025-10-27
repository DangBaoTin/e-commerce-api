# app/models.py
from beanie import Document
from pydantic import EmailStr

class User(Document):
    """
    Represents a User in the database.
    This model is used to interact with the 'users' collection in MongoDB.
    """
    first_name: str
    last_name: str
    email: EmailStr
    hashed_password: str
    is_admin: bool = False

    class Settings:
        name = "users"