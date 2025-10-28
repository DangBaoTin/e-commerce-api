# app/api/v1/endpoints/users.py
from fastapi import APIRouter, HTTPException, status
from app.models import User
from app.schemas import UserCreate, UserOut
from app.security import get_password_hash # <--- IMPORT our new function

router = APIRouter()

@router.post("/", response_model=UserOut, status_code=status.HTTP_201_CREATED)
async def create_user(user_in: UserCreate):
    """
    Create a new user with a hashed password.
    """
    existing_user = await User.find_one(User.email == user_in.email)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered",
        )
    
    # --- THIS IS THE CHANGE ---
    # Use our new security function to hash the password
    hashed_pass = get_password_hash(user_in.password)
    # --------------------------
    
    user = User(
        first_name=user_in.first_name,
        last_name=user_in.last_name,
        email=user_in.email,
        hashed_password=hashed_pass # <-- Store the REAL hash
    )
    
    await user.insert()
    return user

@router.get("/", response_model=list[UserOut])
async def get_all_users():
    """
    Get a list of all users.
    """
    users = await User.find_all().to_list()
    return users