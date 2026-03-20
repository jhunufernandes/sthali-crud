"""{...}."""

from typing import Any

from fastapi import Request
from sthali_core.config import ConfigSchema as BaseConfigSchema


def get_app_context(request: Request) -> dict[str, Any]:
    # yaml_config = config.yaml_config
    crudmodels = request.app.extra.get("crudmodels", [])
    return {
        "title": "Sthali",
        "crudmodels": crudmodels,
    }


def get_context_processors(request: Request) -> dict[str, Any]:
    return {
        "request": request,
        **get_app_context(request),
    }


class ConfigSchema(BaseConfigSchema):
    class CrudmodelSchema(BaseConfigSchema):
        database_uri: str
        dependencies: list[str] | None = None

    crudmodels: CrudmodelSchema
