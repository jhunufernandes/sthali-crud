from typing import Callable

# from .models import Models
# from .crud import CRUD
# from .types import ResourceConfiguration, ResourceSpecification


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


# def config_router(resource_spec: ResourceSpecification, models: Models, crud: CRUD) -> ResourceConfiguration:
#     return ResourceConfiguration(
#         prefix=f'/{resource_spec.name}',
#         routes=[
#             RouteConfiguration(
#                 path='/',
#                 endpoint=replace_type_hint(crud.create, ['resource'], schema.create_input_model),
#                 response_model=schema.create_input_model,
#                 methods=['POST'],
#                 status_code=201),
#             # RouteConfiguration(
#             #     path='/{resource_id}/',
#             #     endpoint=replace_type_hint(crud.read, ['return'], schema.read_resource_model),
#             #     response_model=schema.read_resource_model,
#             #     methods=['GET']),
#             # RouteConfiguration(
#             #     path='/',
#             #     endpoint=replace_type_hint(crud.update, ['resource'], schema.update_resource_model),
#             #     response_model=schema.update_resource_model,
#             #     methods=['PUT']),
#             # RouteConfiguration(
#             #     path='/',
#             #     endpoint=replace_type_hint(crud.update, ['resource'], schema.upsert_resource_model),
#             #     response_model=schema.upsert_resource_model,
#             #     methods=['PUT']),
#             # RouteConfiguration(
#             #     path='/{resource_id}/',
#             #     endpoint=crud.delete,
#             #     response_model=None,
#             #     methods=['DELETE'],
#             #     status_code=204)
#         ],
#         tags=[resource_spec.name]
#     )
