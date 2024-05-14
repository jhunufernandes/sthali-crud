import typing

import pydantic

import sthali_db


@pydantic.dataclasses.dataclass
class FieldDefinition:
    """Field definition"""

    name: str
    type: typing.Any
    default_value: typing.Any = None
    has_default: bool = False  # needed only if default_value is None
    allow_none: bool = False
    description: str | None = None


@pydantic.dataclasses.dataclass
class ResourceSpecification:
    """Resource specification"""

    db: sthali_db.DBSpecification
    name: str
    fields: list[FieldDefinition]


@pydantic.dataclasses.dataclass
class AppSpecification:
    """App specification"""

    resources: list[ResourceSpecification]
    description: str = "A FastAPI package for CRUD operations"
    summary: str | None = None
    title: str = "SthaliCRUD"
    version: str = "0.1.0"


@pydantic.dataclasses.dataclass
class RouteConfiguration:
    """Route Configuration"""

    path: str
    endpoint: typing.Callable[..., typing.Any]
    response_model: typing.Any
    methods: list[typing.Literal["GET", "POST", "PUT", "PATCH", "DELETE"]]
    status_code: int = 200
    dependencies: list = pydantic.Field(default_factory=list)
    name: str | None = None


@pydantic.dataclasses.dataclass
class RouterConfiguration:
    """Router Configuration"""

    prefix: str
    routes: list[RouteConfiguration]
    tags: list[str]
