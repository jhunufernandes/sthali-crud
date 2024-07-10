"""{...}."""
import contextlib
import logging
import typing

import fastapi
import pydantic

import sthali_db

from .config import load_and_parse_spec_file
# from .router import Router

# from .crud import CRUD


@pydantic.dataclasses.dataclass
class ResourceSpecification:
    """Resource specification."""

    db: sthali_db.DBSpecification
    name: str
    fields: list[sthali_db.Field]


@pydantic.dataclasses.dataclass
class AppSpecification:
    """App specification."""

    resources: list[ResourceSpecification]
    description: str = "A FastAPI package for CRUD operations"
    summary: str | None = None
    title: str = "SthaliCRUD"
    version: str = "0.1.0"


@contextlib.asynccontextmanager
async def default_lifespan(app: fastapi.FastAPI):
    logging.info("Startup SthaliCRUD")
    yield
    logging.info("Shutdown SthaliCRUD")


class SthaliCRUD:
    app: fastapi.FastAPI

    def __init__(self, app_spec: AppSpecification, lifespan: typing.Callable = default_lifespan) -> None:
        app = fastapi.FastAPI(
            lifespan=lifespan,
            title=app_spec.title,
            summary=app_spec.summary,
            description=app_spec.description,
            version=app_spec.version,
        )
        self.app = app

        _db: dict[str, sthali_db.DBClient] = {}
        for resource in app_spec.resources:
            models = sthali_db.Models(resource.name, resource.fields)
        #     db = sthali_db.DBClient(resource.db, resource.name)
        #     crud = CRUD(db, models)
        #     router_cfg = config_router(crud, resource.name, models)
        #     router = fastapi.APIRouter(prefix=router_cfg.prefix, tags=router_cfg.tags)  # type: ignore
        #     for route in router_cfg.routes:
        #         router.add_api_route(
        #             path=route.path,
        #             endpoint=route.endpoint,
        #             response_model=route.response_model,
        #             methods=route.methods,  # type: ignore
        #             status_code=route.status_code,
        #             dependencies=route.dependencies,
        #         )

        #     self.app.include_router(router)
        #     _db[resource.name] = db
        self.app.extra["db"] = _db


__all__ = [
    "AppSpecification",
    "SthaliCRUD",
    "load_and_parse_spec_file",
]
