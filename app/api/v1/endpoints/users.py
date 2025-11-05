from fastapi import APIRouter, HTTPException, status, Depends
from app.models.user import User
from app.schemas.user import UserCreate, UserOut
from app.api.dependencies import get_current_user
from app.repositories.user_repository import user_repository

router = APIRouter()

@router.get("/me", response_model=UserOut)
async def get_current_user_profile(
    current_user: User = Depends(get_current_user)
):
    """
    Get profile of the current logged-in user - protected route
    """
    return current_user

@router.post("/", response_model=UserOut, status_code=status.HTTP_201_CREATED)
async def create_user(user_in: UserCreate):
    """
    Create new user
    """
    # Check if user already exists
    existing_user = await user_repository.get_by_email(user_in.email)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered",
        )
    
    # Create the user
    user = await user_repository.create(user_in)
    
    return user

@router.get("/", response_model=list[UserOut])
async def get_all_users():
    """
    Get a list of all users.
    """
    users = await User.find_all().to_list()
    return users