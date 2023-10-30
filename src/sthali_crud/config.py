from typing import Callable

from .crud import CRUD
from .models import Models
from .types import RouteConfiguration, RouterConfiguration


def replace_type_hint(
    original_func: Callable, type_name: str, new_type: type
) -> Callable:
    if original_func.__annotations__ and type_name in original_func.__annotations__:
        original_func.__annotations__[type_name] = new_type
    return original_func


def config_router(crud: CRUD, name: str, models: Models) -> RouterConfiguration:
    return RouterConfiguration(
        prefix=f"/{name}",
        routes=[
            RouteConfiguration(
                path="/",
                endpoint=replace_type_hint(
                    crud.create, "resource", models.create_model
                ),
                response_model=models.response_model,
                methods=["POST"],
                status_code=201,
            ),
            RouteConfiguration(
                path="/{resource_id}/",
                endpoint=crud.read,
                response_model=models.response_model,
                methods=["GET"],
            ),
            RouteConfiguration(
                path="/",
                endpoint=replace_type_hint(
                    crud.update, "resource", models.update_model
                ),
                response_model=models.response_model,
                methods=["PUT"],
            ),
            RouteConfiguration(
                path="/{resource_id}/",
                endpoint=replace_type_hint(
                    crud.update, "resource", models.upsert_model
                ),
                response_model=models.response_model,
                methods=["PUT"],
            ),
            RouteConfiguration(
                path="/{resource_id}/",
                endpoint=crud.delete,
                response_model=None,
                methods=["DELETE"],
                status_code=204,
            ),
            RouteConfiguration(
                path="/",
                endpoint=crud.read_all,
                response_model=list[models.response_model],
                methods=["GET"],
            ),
        ],
        tags=[name],
    )


def parse_spec_file(str) -> dict:
    return {}
