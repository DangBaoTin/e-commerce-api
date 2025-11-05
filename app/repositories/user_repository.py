from app.models.user import User
from app.schemas.user import UserCreate
from app.core.security import get_password_hash
from beanie import PydanticObjectId

class UserRepository:
    async def get_by_email(self, email: str) -> User | None:
        """
        Find user by email address
        """
        return await User.find_one(User.email == email)

    async def get_by_id(self, user_id: PydanticObjectId) -> User | None:
        """
        Find user by ID
        """
        return await User.get(user_id)

    async def create(self, user_in: UserCreate) -> User:
        """
        Create new user
        """
        hashed_password = get_password_hash(user_in.password)
        
        user = User(
            first_name=user_in.first_name,
            last_name=user_in.last_name,
            email=user_in.email,
            hashed_password=hashed_password
        )
        await user.insert()
        return user

user_repository = UserRepository()