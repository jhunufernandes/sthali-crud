"""Configuration schema and request context utilities for sthali-crud."""

from typing import Any

from fastapi import Request
from sthali_core.config import ConfigSchema as BaseConfigSchema


def get_app_context(request: Request) -> dict[str, Any]:
    """Extract application-level context for template rendering.

    Args:
        request: The incoming FastAPI request.

    Returns:
        A dict with the application title and registered CRUD models.
    """
    crudmodels = request.app.extra.get("crudmodels", [])
    return {
        "title": "Sthali",
        "crudmodels": crudmodels,
    }


def get_context_processors(request: Request) -> dict[str, Any]:
    """Build a full Jinja2 context dict including the request and app context.

    Args:
        request: The incoming FastAPI request.

    Returns:
        A dict suitable for passing to a Jinja2 TemplateResponse.
    """
    return {
        "request": request,
        **get_app_context(request),
    }


class ConfigSchema(BaseConfigSchema):
    """Configuration schema for the CRUD layer."""

    class CrudmodelSchema(BaseConfigSchema):
        """Sub-schema for the crudmodels configuration section."""

        database_uri: str
        dependencies: list[str] | None = None

    crudmodels: CrudmodelSchema
