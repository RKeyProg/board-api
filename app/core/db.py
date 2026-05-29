from typing import Annotated, AsyncGenerator
from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import DeclarativeBase
from app.core.settings import Settings
import logging

settings = Settings()

engine = create_async_engine(settings.db.url, echo=False, pool_pre_ping=True)

async_session_local = async_sessionmaker(engine, expire_on_commit=False)

logger = logging.getLogger(__name__)


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_local() as session:
        yield session


async def check_db(session: AsyncSession) -> int:
    result = await session.execute(select(1))
    return result.scalar_one()


DbSessionDep = Annotated[AsyncSession, Depends(get_session)]


class Base(DeclarativeBase):
    pass
