"""Types.
"""
from typing import Any, Callable, Literal, Optional
from pydantic import BaseModel
from pydantic.dataclasses import dataclass


@dataclass
class Field:
    """Field.
    """
    name: str
    type: type
    has_default: bool = False
    default_value: Any = None
    # allow_none: bool = False


class Model(BaseModel):
    pass


class EmptyModel(BaseModel):
    pass


@dataclass
class ResourceSpec:
    """Resource Specification.
    """
    name: str
    fields: list[Field]


@dataclass
class RouteConfig:
    """Route Configuration.
    """
    path: str
    endpoint: Callable[..., Any]
    response_model: Any
    methods: Optional[
        set[Literal['GET', 'POST', 'PUT', 'PATCH', 'DELETE']] | list[Literal['GET', 'POST', 'PUT', 'PATCH', 'DELETE']]
    ] = None
    status_code: int = 200


@dataclass
class ResourceCfg:
    """Resource Configuration.
    """
    prefix: str
    routes: list[RouteConfig]
    tags: Optional[list[str]]
