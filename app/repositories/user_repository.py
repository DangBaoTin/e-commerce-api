# app/repositories/user_repository.py
from app.models import User
from app.schemas import UserCreate
from app.core.security import get_password_hash
from beanie import PydanticObjectId

class UserRepository:
    """
    This class handles all database operations for the User model.
    """

    async def get_by_email(self, email: str) -> User | None:
        """
        Find a user by their email address.
        """
        return await User.find_one(User.email == email)

    async def get_by_id(self, user_id: PydanticObjectId) -> User | None:
        """
        Find a user by their ID.
        """
        return await User.get(user_id)

    async def create(self, user_in: UserCreate) -> User:
        """
        Create a new user in the database.
        """
        # Hashing logic is part of user creation, so it lives here.
        hashed_password = get_password_hash(user_in.password)
        
        user = User(
            first_name=user_in.first_name,
            last_name=user_in.last_name,
            email=user_in.email,
            hashed_password=hashed_password
        )
        await user.insert()
        return user

# Create a single instance that our services can use
user_repository = UserRepository()