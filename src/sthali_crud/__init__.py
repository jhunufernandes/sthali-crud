from fastapi import APIRouter, FastAPI
from .config import config_router
from .crud import CRUD
from .db import DB
from .schema import Schema
from .types import Field, ResourceSpec


class SthaliCRUD:
    """SthaliCRUD client
    """
    _app = FastAPI()

    def __init__(self, resource_spec: ResourceSpec, db: DB = DB()) -> None:
        schema = Schema(resource_spec.name, resource_spec.fields)
        crud = CRUD(db, schema.model)
        resource_cfg = config_router(resource_spec, schema, crud)
        router = APIRouter(prefix=resource_cfg.prefix, tags=resource_cfg.tags)
        for route in resource_cfg.routes:
            router.add_api_route(path=route.path,
                                 endpoint=route.endpoint,
                                 response_model=route.response_model,
                                 methods=route.methods,
                                 status_code=route.status_code)
        self._app.include_router(router)

    @property
    def app(self) -> FastAPI:
        """app property

        Returns:
            FastAPI: Fastapi client
        """
        return self._app


__all__ = [
    'DB',
    'Field',
    'ResourceSpec',
    'SthaliCRUD',
]
