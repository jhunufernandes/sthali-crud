"""Types.
"""
from typing import Any, Callable, Literal
from pydantic import BaseModel
from pydantic.dataclasses import dataclass


# @dataclass
# class RouteConfiguration:
#     """Route Configuration.
#     """
#     path: str
#     endpoint: Callable[..., Any]
#     response_model: Any
#     methods: list[Literal['GET', 'POST', 'PUT', 'PATCH', 'DELETE']] | None = None
#     status_code: int = 200


# @dataclass
# class RouterConfiguration:
#     """Router Configuration.
#     """
#     prefix: str
#     routes: list[RouteConfiguration]
#     tags: list[str]


@dataclass
class ModelStrategy:
    """Model strategy
    """
    create_input_model: type[BaseModel]
    upsert_input_model: type[BaseModel]
    update_input_model: type[BaseModel]
    response_model: type[BaseModel]


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
