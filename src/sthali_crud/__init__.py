"""{...}."""

from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from .database.models import RoleModel
from .database.schemas import RoleCreateSchema, RoleSchema
from .routers.api import API
from .routers.views import VIEWS


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """A context manager that handles the startup and shutdown of Sthali application.

    Args:
        app (FastAPI): The FastAPI application instance.

    Yields:
        None
    """
    # Test DB connection at startup
    # try:
    #     DbSession
    #     async for conn in get_connection():
    #         result = await conn.execute(sqlalchemy.text("SELECT 1"))
    #         value = result.scalar()
    #         if value != 1:
    #             raise RuntimeError("Database test query failed")
    #         break  # Only need one connection test
    # except Exception as e:
    #     print(f"Database connection failed: {e}")
    #     raise
    # app.extra["git_revision"] = config.git_revision
    yield


app = FastAPI(lifespan=lifespan)
app.mount("/static", StaticFiles(directory=str(Path(__file__).parent / "static")), name="static")
api = API(RoleModel, RoleSchema, RoleCreateSchema, RoleCreateSchema)
views = VIEWS(RoleModel, RoleSchema, RoleCreateSchema, RoleCreateSchema)
app.include_router(api.api_router, prefix="/api/v1")
app.include_router(views.api_router, prefix="/views")
