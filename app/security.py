# app/security.py
from passlib.context import CryptContext

# 1. Create a CryptContext instance
# We specify the 'bcrypt' scheme and mark it as the default
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verifies a plain-text password against a stored hash.
    """
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    """
    Hashes a plain-text password.
    """
    return pwd_context.hash(password)