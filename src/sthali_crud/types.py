from __future__ import annotations
from typing import Any, Callable, Literal
from uuid import UUID, uuid4
from pydantic import BaseModel, ConfigDict, Field
from pydantic.dataclasses import dataclass


class CreateModel(BaseModel):
    """Create Model.
    """


class ResponseModel(BaseModel):
    """Response Model.
    """
    id: UUID


class UpdateModel(BaseModel):
    """Update Model.
    """
    id: UUID | None = None


class UpsertModel(BaseModel):
    """Upsert Model.
    """
    id: UUID = Field(default_factory=uuid4)

    model_config = ConfigDict(extra='allow')


@dataclass
class ModelStrategy:
    """Model strategy.
    """
    create_model: type[CreateModel]
    response_model: type[ResponseModel]
    update_model: type[UpdateModel]
    upsert_model: type[UpsertModel]


@dataclass
class FieldDefinition:
    """Field definition.
    """
    name: str
    type: type
    has_default: bool = False
    default_value: Any = None
    allow_none: bool = False


@dataclass
class ResourceSpecification:
    """Resource specification.
    """
    name: str
    fields: list[FieldDefinition]


@dataclass
class RouteConfiguration:
    """Route Configuration.
    """
    path: str
    endpoint: Callable[..., Any]
    response_model: Any
    methods: list[Literal['GET', 'POST', 'PUT', 'PATCH', 'DELETE']]
    status_code: int = 200


@dataclass
class RouterConfiguration:
    """Router Configuration.
    """
    prefix: str
    routes: list[RouteConfiguration]
    tags: list[str]
