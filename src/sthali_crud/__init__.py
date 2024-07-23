"""{...}."""

from collections.abc import Callable
from contextlib import asynccontextmanager
from logging import info
from typing import Any, Annotated

from fastapi import FastAPI
from pydantic import Field
from pydantic.dataclasses import dataclass

from sthali_db import DB, DBSpecification, FieldDefinition, Models

from .config import load_and_parse_spec_file
from .crud import CRUD
from .router import Router


@dataclass
class ResourceSpecification:
    """Represents the specification of the resource.

    Attributes:
        db (DBSpecification): The database specification for the resource.
        name (str): The name of the resource.
        fields (list[FieldDefinition]): The list of field definitions for the resource.
    """

    db: Annotated[DBSpecification, Field(description="The database specification for the resource")]
    name: Annotated[str, Field(description="The name of the resource")]
    fields: Annotated[list[FieldDefinition], Field(description="The list of field definitions for the resource")]


@dataclass
class AppSpecification:
    """Represents the specification of a SthaliCRUD application.

    Attributes:
        resources (List[ResourceSpecification]): The list of resource specifications.
        description (str): The description of the application. Default value is "A FastAPI package for CRUD operations".
        summary (str | None): The summary of the application. Default value is None.
        title (str): The title of the application. Default value is "SthaliCRUD".
        version (str): The version of the application. Default value is "0.1.0".
    """

    resources: Annotated[
        list[ResourceSpecification], Field(default_factory=list, description="The list of resource specifications")
    ]
    description: Annotated[
        str, Field(default="A FastAPI package for CRUD operations", description="The description of the application")
    ]
    summary: Annotated[str | None, Field(default=None, description="The summary of the application")]
    title: Annotated[str, Field(default="SthaliCRUD", description="The title of the application")]
    version: Annotated[str, Field(default="0.1.0", description="The version of the application")]


@asynccontextmanager
async def default_lifespan(app: FastAPI):
    """A context manager that handles the startup and shutdown of SthaliCRUD.

    Args:
        app (FastAPI): The FastAPI application instance.

    Yields:
        None
    """
    info("Startup SthaliCRUD")
    yield
    info("Shutdown SthaliCRUD")


class SthaliCRUD:
    def __init__(self, app_spec: AppSpecification, lifespan: Callable[..., Any] = default_lifespan) -> None:
        app = FastAPI(
            lifespan=lifespan,
            title=app_spec.title,
            summary=app_spec.summary,
            description=app_spec.description,
            version=app_spec.version,
        )
        self.app = app

        _db: dict[str, DB] = {}
        for resource in app_spec.resources:
            models = Models(resource.name, resource.fields)
            db = DB(resource.db, resource.name)
            crud = CRUD(db, models)
            router = Router(crud, resource.name, models)
            self.app.include_router(router.api_router)
            _db[resource.name] = db
        self.app.extra["db"] = _db


__all__ = [
    "AppSpecification",
    "SthaliCRUD",
    "load_and_parse_spec_file",
]
