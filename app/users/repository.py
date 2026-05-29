import logging
from typing import Annotated
from fastapi import Depends
from sqlalchemy import select
from app.core.db import DbSessionDep
from app.users.model import User

logger = logging.getLogger(__name__)


class UserRepository:
    def __init__(self, db_session: DbSessionDep):
        self.db_session = db_session

    async def get_by_email(self, email: str):
        result = await self.db_session.execute(select(User).where(User.email == email))
        return result.scalar_one_or_none()

    async def save(self, user: User):
        self.db_session.add(user)
        await self.db_session.commit()
        await self.db_session.refresh(user)
        return user


def get_user_repository(db_session: DbSessionDep) -> UserRepository:
    return UserRepository(db_session)


UserRepositoryDep = Annotated[UserRepository, Depends(get_user_repository)]
