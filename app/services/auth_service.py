from typing import Optional
from app.repositories.user_repository import user_repository, UserRepository
from app.core.security import verify_password, create_access_token

class AuthService:
    def __init__(self, user_repo: UserRepository = user_repository):
        self.user_repo = user_repo

    async def login(self, username: str, password: str) -> Optional[str]:
        user = await self.user_repo.get_by_email(username)

        if not user or not verify_password(password, user.hashed_password):
            return None

        access_token = create_access_token(
            data={"sub": user.email}
        )
        return access_token

auth_service = AuthService()