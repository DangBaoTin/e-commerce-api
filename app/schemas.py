from pydantic import BaseModel, EmailStr

class UserCreate(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    password: str # We get a plain password, then hash it

class UserOut(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    is_admin: bool

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: str | None = None