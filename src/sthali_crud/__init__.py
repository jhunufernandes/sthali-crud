"""Main application class for Sthali CRUD operations."""

from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager
from logging import getLogger
from typing import Any

from fastapi import FastAPI
from sthali_core.config import Config
from sthali_db import Engine, ModelType, SchemaType, definitions_type

from .routers import Base as BaseRouter
from .routers.api import API

__all__ = [
    "SthaliCRUD",
]


logger = getLogger(__name__)


@asynccontextmanager
async def lifespan(_app: FastAPI) -> AsyncGenerator[None, None]:
    """Handle startup and shutdown of the Sthali application.

    Yields:
        None
    """
    try:
        logger.info("Database connection successful")
    except RuntimeError as e:
        message = f"Database connection failed: {e}"
        logger.exception(message)
        raise

    yield

    logger.info("Application shutting down")


class SthaliCRUD:
    """FastAPI application for Sthali CRUD operations."""

    def __init__(
        self,
        config: Config,
        definitions: definitions_type,
        extended_routers: list[type[BaseRouter]] | None = None,
        dependencies: dict[str, Any] | None = None,
    ) -> None:
        """Initialize the Sthali CRUD FastAPI application.

        Args:
            config: Application configuration providing the database URI.
            definitions: List of (Model, (CreateSchema, ReadSchema, UpdateSchema)) tuples.
            extended_routers: Additional router classes registered for each model.
            dependencies: FastAPI dependencies keyed by name (e.g. "api_key").
        """
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
        """Register an API router for the given model and schemas.

        Args:
            model: The SQLAlchemy model class.
            schemas: Tuple of (CreateSchema, ReadSchema, UpdateSchema) classes.
            router: The router class to instantiate.
            *args: Additional positional arguments forwarded to the router constructor.
            **kwargs: Additional keyword arguments forwarded to the router constructor.

        Returns:
            The instantiated and registered router.
        """
        _router = router(self.engine.db_session, model, *schemas, *args, **kwargs)
        if not _router.prefix:
            msg = "Router prefix is not set"
            raise ValueError(msg)
        self.app.include_router(_router.api_router, prefix=_router.prefix, dependencies=[self.dependencies["api_key"]])
        return _router
