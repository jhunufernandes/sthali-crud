"""Types.
"""
from enum import Enum
from typing import Any, Callable, Literal, Optional, Union

from pydantic.dataclasses import dataclass


@dataclass
class Field:
    """Field.
    """
    name: str
    type: type
    default: Any = None
    allow_none: bool = False


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
