from unittest.mock import AsyncMock

from src.sthali_crud.crud import CRUD
from src.sthali_crud.models import Models
from src.sthali_crud.types import (
    DBSpecification,
    FieldDefinition,
    ResourceSpecification,
    RouteConfiguration,
    RouterConfiguration,
)

RESOURCE_SPEC = ResourceSpecification(
    db=DBSpecification(
        engine="tinydb",
        path="",
    ),
    name="people",
    fields=[
        FieldDefinition(
            name="name",
            type=str,
        ),
        FieldDefinition(
            name="age",
            type=int,
        ),
    ],
)


class MockModels(Models):
    create_model = AsyncMock(return_value=dict)
    response_model = AsyncMock(return_value=dict)
    update_model = AsyncMock(return_value=dict)
    upsert_model = AsyncMock(return_value=dict)


class MockCRUD(CRUD):
    create = AsyncMock(return_value={})
    read = AsyncMock(return_value={})
    update = AsyncMock(return_value={})
    upsert = AsyncMock(return_value={})
    delete = AsyncMock(return_value=None)


__all__ = [
    "FieldDefinition",
    "ResourceSpecification",
    "RouterConfiguration",
    "RouteConfiguration",
]
