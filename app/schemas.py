# app/schemas.py
from pydantic import BaseModel, EmailStr

class UserCreate(BaseModel):
    """
    Pydantic model for creating a new user.
    Used for request body validation in the API.
    """
    first_name: str
    last_name: str
    email: EmailStr
    password: str # We get a plain password, then hash it

class UserOut(BaseModel):
    """
    Pydantic model for sending user data to the client.
    Used for the API response. Note: no password!
    """
    first_name: str
    last_name: str
    email: EmailStr
    is_admin: bool