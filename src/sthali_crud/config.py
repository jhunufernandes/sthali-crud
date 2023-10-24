from typing import Any, Callable
from .models import Models
from .crud import CRUD
from .types import ResourceSpecification, RouteConfiguration, RouterConfiguration


class Config:
    """Config main class.
    """
    _router_cfg: RouterConfiguration

    def __init__(self, crud: CRUD, models: Models, resource_spec: ResourceSpecification) -> None:
        self._router_cfg = self.config_router(crud, models, resource_spec)

    @property
    def router_cfg(self) -> RouterConfiguration:
        """router_cfg property.

        Returns:
            RouterConfiguration: API routes definition.
        """
        return self._router_cfg

    @staticmethod
    def replace_type_hint(original_func: Callable, type_name: str, new_type: type) -> Callable:
        """Replace type hint annotations.

        Args:
            original_func (function): Function that will have __annotations__ replaced.
            type_name (str): Annotation name key to be replaced.
            new_type (type): New type.

        Returns:
            Callable: Original function.
        """
        if original_func.__annotations__ and type_name in original_func.__annotations__:
            original_func.__annotations__[type_name] = new_type
        return original_func

    @staticmethod
    def config_router(crud: CRUD, models: Models, resource_spec: ResourceSpecification) -> RouterConfiguration:
        """Parse spec and generate routes.

        Args:
            crud (CRUD): CRUD class instance.
            models (Models): Models class instance.
            resource_spec (ResourceSpecification): Resource fields definition.

        Returns:
            RouterConfiguration: API routes definition.
        """
        return RouterConfiguration(
            prefix=f'/{resource_spec.name}',
            routes=[
                RouteConfiguration(
                    path='/',
                    endpoint=Config.replace_type_hint(crud.create, 'resource', models.create_model),
                    response_model=models.response_model,
                    methods=['POST'],
                    status_code=201),
                RouteConfiguration(
                    path='/{resource_id}/',
                    endpoint=crud.read,
                    response_model=models.response_model,
                    methods=['GET']),
                RouteConfiguration(
                    path='/',
                    endpoint=Config.replace_type_hint(crud.update, 'resource', models.update_model),
                    response_model=models.response_model,
                    methods=['PUT']),
                RouteConfiguration(
                    path='/{resource_id}/',
                    endpoint=Config.replace_type_hint(crud.update, 'resource', models.update_model),
                    response_model=models.response_model,
                    methods=['PUT']),
                RouteConfiguration(
                    path='/{resource_id}/',
                    endpoint=crud.delete,
                    response_model=None,
                    methods=['DELETE'],
                    status_code=204),
            ],
            tags=[resource_spec.name]
        )
