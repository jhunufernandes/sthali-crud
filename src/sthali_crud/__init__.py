from fastapi import APIRouter, FastAPI
from .config import replace_type_hint
from .crud import CRUD
from .db import DB
from .models import Models
from .types import FieldDefinition, ResourceSpecification


class SthaliCRUD:
    _app = FastAPI()

    @property
    def app(self) -> FastAPI:
        return self._app

    def __init__(self, resource_spec: ResourceSpecification, db: DB) -> None:
        _models: Models = Models(resource_spec)
        _crud: CRUD = CRUD(db=db, models=_models)
        # _crud.replace_model(_models.create_input_model)
        # _router_cfg: RouterConfiguration = config_router(resource_spec=resource_spec, models=_models, crud=_crud)
        _router = APIRouter(prefix=f'/{resource_spec.name}', tags=[resource_spec.name])
        _router.add_api_route(
            path='/',
            endpoint=replace_type_hint(_crud.create, ['resource'], _models.create_input_model),
            response_model=_models.response_model,
            methods=['POST'],
            status_code=201)

        self._app.include_router(_router)


__all__ = [
    'DB',
    'FieldDefinition',
    'ResourceSpecification',
    'SthaliCRUD',
]
