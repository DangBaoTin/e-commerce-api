# app/services/auth_service.py
from typing import Optional
from app.repositories.user_repository import user_repository, UserRepository
from app.core.security import verify_password, create_access_token

class AuthService:
    def __init__(self, user_repo: UserRepository = user_repository):
        """
        Initialize the service with the user repository.
        We use dependency injection, but default to the global instance.
        """
        self.user_repo = user_repo

    async def login(self, username: str, password: str) -> Optional[str]:
        """
        Handles the business logic for user login.
        Returns a JWT token if successful, None otherwise.
        """
        # 1. Find user
        user = await self.user_repo.get_by_email(username)

        # 2. Verify user and password
        if not user or not verify_password(password, user.hashed_password):
            return None  # Authentication failed

        # 3. Create and return token
        access_token = create_access_token(
            data={"sub": user.email}
        )
        return access_token

# Create a single instance that our endpoints can use
auth_service = AuthService()