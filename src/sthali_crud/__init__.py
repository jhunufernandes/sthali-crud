import typing

import fastapi

import sthali_db

from .config import config_router, default_lifespan, load_and_parse_spec_file
from .crud import CRUD
from .models import Models
from .types import AppSpecification


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

        _db: dict[str, sthali_db.DBEngine] = {}
        for resource in app_spec.resources:
            models = Models(resource.name, resource.fields)
            db = sthali_db.DBEngine(resource.db, resource.name)
            crud = CRUD(db, models)
            router_cfg = config_router(crud, resource.name, models)
            router = fastapi.APIRouter(prefix=router_cfg.prefix, tags=router_cfg.tags)  # type: ignore
            for route in router_cfg.routes:
                router.add_api_route(
                    path=route.path,
                    endpoint=route.endpoint,
                    response_model=route.response_model,
                    methods=route.methods,  # type: ignore
                    status_code=route.status_code,
                    dependencies=route.dependencies,
                )

            self.app.include_router(router)
            _db[resource.name] = db
        self.app.extra["db"] = _db


__all__ = [
    "AppSpecification",
    "load_and_parse_spec_file",
    "SthaliCRUD",
]
