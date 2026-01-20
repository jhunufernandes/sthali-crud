"""Database engine and session management.

This module provides the SQLAlchemy async engine, session factory,
and FastAPI dependency for database connections.
"""

from collections.abc import AsyncGenerator
from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from ..config import config

engine = create_async_engine(
    config.database_uri,
    echo=True,
    pool_pre_ping=True,
)


async_session_maker = async_sessionmaker(
    engine,
    expire_on_commit=False,
    class_=AsyncSession,
)


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """Provide an asynchronous database session.

    This function serves as a FastAPI dependency that creates and manages
    database sessions. It ensures proper cleanup after each request.

    Returns:
        AsyncSession: An active database session.

    """
    async with async_session_maker() as session:
        try:
            yield session
        finally:
            await session.close()


DbSession = Annotated[AsyncSession, Depends(get_db)]
