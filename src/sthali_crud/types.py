from typing import Any, Callable, Literal

from pydantic.dataclasses import dataclass

from src.sthali_crud.db_engines import AVAILABLE_ENGINES


@dataclass
class FieldDefinition:
    """Field definition"""

    name: str
    type: type
    has_default: bool = False  # needed only if default_value is None
    default_value: Any = None
    allow_none: bool = False


@dataclass
class ResourceSpecification:
    """Resource specification"""

    db_engine: Literal[AVAILABLE_ENGINES]
    name: str
    fields: list[FieldDefinition]


@dataclass
class AppSpecification:
    """App specification"""

    resources: list[ResourceSpecification]


@dataclass
class RouteConfiguration:
    """Route Configuration"""

    path: str
    endpoint: Callable[..., Any]
    response_model: Any
    methods: list[Literal["GET", "POST", "PUT", "PATCH", "DELETE"]]
    status_code: int = 200


@dataclass
class RouterConfiguration:
    """Router Configuration"""

    prefix: str
    routes: list[RouteConfiguration]
    tags: list[str]
