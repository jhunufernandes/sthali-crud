from fastapi import APIRouter, FastAPI

from .config import Config
from .crud import CRUD
from .db import DB
from .models import Models
from .types import FieldDefinition, ResourceSpecification


class SthaliCRUD:
    """SthaliCRUD main class."""

    _app: FastAPI = FastAPI()
    _db: DB

    @property
    def app(self) -> FastAPI:
        """app property.

        Returns:
            FastAPI: FastAPI client.
        """
        return self._app

    @property
    def db(self) -> DB:
        """db property.

        Returns:
            FastAPI: FastAPI client.
        """
        return self._db

    def __init__(self, db: DB, resource_spec: ResourceSpecification) -> None:
        self._db = db
        _models = Models(resource_spec)
        _crud = CRUD(db, _models)
        _config = Config(_crud, _models, resource_spec)
        _router_cfg = _config.router_cfg
        _router = APIRouter(prefix=_router_cfg.prefix, tags=_router_cfg.tags)
        for _route in _router_cfg.routes:
            _router.add_api_route(
                path=_route.path,
                endpoint=_route.endpoint,
                response_model=_route.response_model,
                methods=_route.methods,
                status_code=_route.status_code,
            )
        self._app.include_router(_router)


__all__ = [
    "DB",
    "FieldDefinition",
    "ResourceSpecification",
    "SthaliCRUD",
]
