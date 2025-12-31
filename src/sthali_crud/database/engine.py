"""{...}."""

from collections.abc import AsyncGenerator
from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from ..config import config

engine = create_async_engine(
    config.database_uri,
    echo=True,
    connect_args={"check_same_thread": False},
)


async_session = async_sessionmaker(
    engine,
    expire_on_commit=False,
    class_=AsyncSession,
)


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """{...}."""
    async with async_session() as session:
        yield session


DbSession = Annotated[AsyncSession, Depends(get_db)]
