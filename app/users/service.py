import logging
from typing import Annotated

from fastapi import Depends
from app.users.jwt import create_access_token
from app.users.model import User
from app.users.repository import UserRepository, UserRepositoryDep
from app.users.schema import UserLoginRequest, UserRegisterRequest
from app.users.security import hash_password, verify_password

logger = logging.getLogger(__name__)


class UserService:
    def __init__(self, user_repo: UserRepository):
        self.user_repo = user_repo

    async def create(self, user_data: UserRegisterRequest):
        user = await self.user_repo.get_by_email(user_data.email)
        if user:
            raise ValueError("User already exists")

        hashed_password = hash_password(user_data.password)
        user = User(email=user_data.email, hashed_password=hashed_password)
        saved_user = await self.user_repo.save(user)
        token = create_access_token(saved_user.id)
        return token

    async def authenticate(self, user_data: UserLoginRequest):
        user = await self.user_repo.get_by_email(user_data.email)
        if not user:
            return None
        if not verify_password(user_data.password, user.hashed_password):
            return None
        return create_access_token(user.id)


def get_user_service(user_repo: UserRepositoryDep):
    return UserService(user_repo)


UserServiceDep = Annotated[UserService, Depends(get_user_service)]
