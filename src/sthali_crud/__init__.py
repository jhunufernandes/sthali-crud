"""{...}."""

from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager
from logging import getLogger

from fastapi import FastAPI
from sthali_db import Engine, ModelType, SchemaType, definitions_type

from .routers import Base as BaseRouter
from .routers.api import API

__all__ = [
    "CRUDSchemas",
    "CRUDTemplates",
    "SthaliCRUD",
]


logger = getLogger(__name__)



@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """A context manager that handles the startup and shutdown of Sthali application.

    Args:
        app (FastAPI): The FastAPI application instance.

    Yields:
        None
    """
    try:
        # engine = Engine.load_from_config(config.yaml_config["crudmodels"]["database_uri"])
        # await engine.test_db()
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
        config,
        definitions: definitions_type,
        extended_routers: list[type[BaseRouter]] | None = None,
        dependencies: dict | None = None,
    ) -> None:
        """Initialize the Sthali CRUD FastAPI application."""
        self.engine = Engine.load_from_config(config.yaml_config["crudmodels"]["database_uri"])
        self.dependencies = dependencies

        app = FastAPI(lifespan=lifespan)
        self.app = app
        self.definitions = definitions

        self.app.extra["crudmodels"] = {}
        for model, schemas in definitions or []:
            api = self.register_api_router(model, schemas, API)
            self._extend_crudmodels(api)

            for router in extended_routers or []:
                self.register_api_router(model, schemas, router, api=api)

    def _extend_crudmodels(self, api: BaseRouter) -> None:
        resource_name = api.resource_name
        model_json_schema = api.read_schema.model_json_schema()
        self.app.extra["crudmodels"][resource_name] = {
            "table": resource_name,
            "title": model_json_schema.get("title", resource_name),
            "view_read_many": f"/views/{resource_name}",
            "api": api,
        }

    def register_api_router(
        self,
        model: ModelType,
        schemas: tuple[SchemaType, SchemaType, SchemaType],
        router: type[BaseRouter],
        *args,
        **kwargs,
    ) -> BaseRouter:
        _router = router(self.engine.db_session, model, *schemas, *args, **kwargs)
        if not _router.prefix:
            msg = "Router prefix is not set"
            raise ValueError(msg)
        self.app.include_router(_router.api_router, prefix=_router.prefix, dependencies=[self.dependencies["api_key"]])
        return _router
