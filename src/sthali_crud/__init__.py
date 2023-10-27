from fastapi import APIRouter, FastAPI

from src.sthali_crud.config import config_router
from src.sthali_crud.crud import CRUD
from src.sthali_crud.db import DB
from src.sthali_crud.models import Models
from src.sthali_crud.types import AppSpecification


class SthaliCRUD:
    app: FastAPI = FastAPI()

    def __init__(self, app_spec: AppSpecification) -> None:
        for resource in app_spec.resources:
            models = Models(resource.name, resource.fields)
            db = DB(resource.db_engine, resource.name)
            crud = CRUD(db, models)
            router_cfg = config_router(crud, resource.name, models)
            router = APIRouter(prefix=router_cfg.prefix, tags=router_cfg.tags)
            for route in router_cfg.routes:
                router.add_api_route(
                    path=route.path,
                    endpoint=route.endpoint,
                    response_model=route.response_model,
                    methods=route.methods,
                    status_code=route.status_code,
                )
            self.app.include_router(router)


__all__ = [
    "AppSpecification",
    "SthaliCRUD",
]
