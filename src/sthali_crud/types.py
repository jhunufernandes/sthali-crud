from typing import Any, Callable, Literal

from pydantic import Field, dataclasses

from sthali_db import DBSpecification


@dataclasses.dataclass
class FieldDefinition:
    """Field definition"""

    name: str
    type: Any
    has_default: bool = False  # needed only if default_value is None
    default_value: Any = None


@dataclasses.dataclass
class ResourceSpecification:
    """Resource specification"""

    db: DBSpecification
    name: str
    fields: list[FieldDefinition]


@dataclasses.dataclass
class AppSpecification:
    """App specification"""

    resources: list[ResourceSpecification]
    description: str = "A FastAPI package for CRUD operations"
    summary: str | None = None
    title: str = "SthaliCRUD"
    version: str = "0.1.0"


@dataclasses.dataclass
class RouteConfiguration:
    """Route Configuration"""

    path: str
    endpoint: Callable[..., Any]
    response_model: Any
    methods: list[Literal["GET", "POST", "PUT", "PATCH", "DELETE"]]
    status_code: int = 200
    dependencies: list = Field(default_factory=list)


@dataclasses.dataclass
class RouterConfiguration:
    """Router Configuration"""

    prefix: str
    routes: list[RouteConfiguration]
    tags: list[str]
