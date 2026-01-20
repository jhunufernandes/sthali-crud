"""{...}."""

import logging
from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.applications import Lifespan
from fastapi.staticfiles import StaticFiles

from .crud import CRUD
from .database.engine import async_session_maker, test_db
from .database.models import BaseModel
from .database.schemas import BaseSchema

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """A context manager that handles the startup and shutdown of Sthali application.

    Args:
        app (FastAPI): The FastAPI application instance.

    Yields:
        None
    """
    try:
        await test_db(async_session_maker)
        logger.info("Database connection successful")
    except RuntimeError as e:
        message = f"Database connection failed: {e}"
        logger.exception(message)
        raise

    yield

    # Cleanup on shutdown if needed
    logger.info("Application shutting down")


class SthaliCRUD:
    """FastAPI application for Sthali CRUD operations."""

    def __init__(
        self,
        lifespan: Lifespan,
        static: StaticFiles,
        model: type[BaseModel],
        create_schema: type[BaseSchema],
        read_schema: type[BaseSchema],
        update_schema: type[BaseSchema],
        create_template: str,
        read_template: str,
        read_many_template: str,
    ) -> None:
        """Initialize the Sthali CRUD FastAPI application."""
        app = FastAPI(lifespan=lifespan)
        # app.mount("/static", StaticFiles(directory=str(Path(__file__).parent / "static")), name="static")
        app.mount("/static", static, name="static")
        crud = CRUD(
            model,
            read_schema,
            create_schema,
            update_schema,
            create_template,
            read_template,
            read_many_template,
        )
        app.include_router(crud.api.api_router, prefix="/api/v1")
        app.include_router(crud.views.api_router, prefix="/views")
