from contextlib import asynccontextmanager

from fastapi import APIRouter, FastAPI

from .config import config_router
from .crud import CRUD
from .db import DB
from .models import Models
from .types import AppSpecification


@asynccontextmanager
async def lifespan(app: FastAPI):
    print('startup event')
    yield
    print('shutdown event')


class SthaliCRUD:
    app: FastAPI

    def __init__(self, app_spec: AppSpecification, lifespan: callable = lifespan) -> None:
        app = FastAPI(lifespan=lifespan)
        self.app = app

        for resource in app_spec.resources:
            models = Models(resource.name, resource.fields)
            db = DB(resource.db, resource.name)
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
