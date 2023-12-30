from typing import Callable

from fastapi import APIRouter, FastAPI

from .config import config_router, default_lifespan, load_and_parse_spec_file
from .crud import CRUD
from .db import DB
from .models import Models
from .types import AppSpecification


class SthaliCRUD:
    app: FastAPI

    def __init__(self, app_spec: AppSpecification, lifespan: Callable = default_lifespan) -> None:
        app = FastAPI(lifespan=lifespan)
        self.app = app

        _db: dict[str, DB] = {}
        for resource in app_spec.resources:
            models = Models(resource.name, resource.fields)
            db = DB(resource.db, resource.name)
            crud = CRUD(db, models)
            router_cfg = config_router(crud, resource.name, models)
            router = APIRouter(prefix=router_cfg.prefix, tags=router_cfg.tags)  # type: ignore
            for route in router_cfg.routes:
                router.add_api_route(
                    path=route.path,
                    endpoint=route.endpoint,
                    response_model=route.response_model,
                    methods=route.methods,  # type: ignore
                    status_code=route.status_code,
                )

            self.app.include_router(router)
            _db[resource.name] = db
        self.app.extra["db"] = _db


__all__ = [
    "AppSpecification",
    "load_and_parse_spec_file",
    "SthaliCRUD",
]
