"""Sthali CRUD client.
"""
from fastapi import APIRouter, FastAPI
from .config import config_router
from .crud import CRUD
from .db import DB
from .helpers import ModelClass
from .schema import Schema
from .types import Field, Model, ResourceSpec


class SthaliCRUD(ModelClass):
    """SthaliCRUD client
    """
    _app = FastAPI()

    def __init__(self, _resource_spec: ResourceSpec, _db: DB = DB()) -> None:
        _schema = Schema(_resource_spec.name, _resource_spec.fields)
        _crud = CRUD(db=_db, model=_schema.model)
        _resource_cfg = config_router(_resource_spec, _schema, _crud)
        _router = APIRouter(prefix=_resource_cfg.prefix, tags=_resource_cfg.tags)
        for route in _resource_cfg.routes:
            _router.add_api_route(path=route.path,
                                  endpoint=route.endpoint,
                                  response_model=route.response_model,
                                  methods=route.methods,
                                  status_code=route.status_code)
        self._app.include_router(_router)
        self._model = _schema.model

    @property
    def app(self) -> FastAPI:
        """App property.

        Returns:
            FastAPI: Fastapi client.
        """
        return self._app


__all__ = [
    'DB',
    'Field',
    'Model',
    'ResourceSpec',
    'SthaliCRUD',
]
