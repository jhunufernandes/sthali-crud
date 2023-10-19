"""Config functions.
"""
from typing import Any, Callable
from .crud import CRUD
from .schema import Schema
from .types import ResourceCfg, ResourceSpec, RouteConfig


def replace_type_hint(original_func: Callable, type_names: list[str], new_type: type) -> Callable:
    """Replace type hint.

    Args:
        original_func (function): Function that will have __annotations__ replaced.
        type_names (list[str] | set[str]): List of __annotations__ keys to be replaced.
        new_type (type): New type.

    Returns:
        Callable: Original function.
    """
    for name in type_names:
        original_func.__annotations__[name] = new_type
    return original_func


def config_router(resource_spec: ResourceSpec, schema: Schema, crud: CRUD) -> ResourceCfg:
    """Config router.

    Args:
        resource_spec (ResourceSpec): Resource specification.
        schema (Schema): Schema.
        crud (CRUD): CRUD.

    Returns:
        ResourceCfg: Resource configuration.
    """

    model = schema.model
    return ResourceCfg(
        prefix=f'/{resource_spec.name}',
        routes=[
            RouteConfig(
                path='/',
                endpoint=replace_type_hint(crud.create, ['resource'], model),
                response_model=model,
                methods=['POST'],
                status_code=201),
            RouteConfig(
                path='/{resource_id}/',
                endpoint=replace_type_hint(crud.read, ['return'], model),
                response_model=model,
                methods=['GET']),
            RouteConfig(
                path='/',
                endpoint=replace_type_hint(crud.update, ['resource'], model),
                response_model=model,
                methods=['PUT']),
            # RouteConfig(
            #     path='/{resource_id}/',
            #     endpoint=crud.delete,
            #     response_model=None,
            #     methods=['DELETE'],
            #     status_code=204)
        ],
        tags=[resource_spec.name]
    )
