from collections.abc import Callable
from functools import wraps
from typing import Annotated, Any, List, Literal

from fastapi import APIRouter
from pydantic import Field
from pydantic.dataclasses import dataclass

from sthali_db import Models

from .crud import CRUD


@dataclass
class Route:
    """Represents a route in the application.

    Attributes:
        path (str): The URL path for the route.
        endpoint (Callable[..., Any]): The function that handles the route.
        response_model (Any): The response model for the route.
        methods (list[str]): The HTTP methods supported by the route.
        status_code (int): The HTTP status code for the response. Default is 200.
        dependencies (list): The dependencies for the route. Default is an empty list.
        name (str | None): The name of the route. Default is None.
    """

    path: Annotated[str, Field(description="The URL path for the route")]
    endpoint: Annotated[Callable[..., Any], Field(description="The function that handles the route")]
    response_model: Annotated[Any, Field(description="The response model for the route")]
    methods: Annotated[
        list[Literal["GET", "POST", "PUT", "PATCH", "DELETE"]],
        Field(description="The HTTP methods supported by the route"),
    ]
    status_code: Annotated[int, Field(default=200, description="The HTTP status code for the response")]
    dependencies: Annotated[list, Field(default=[], description="The dependencies for the route")]
    name: Annotated[str | None, Field(description="The name of the route")] = None


@dataclass
class RouterConfiguration:
    """Represents the configuration for a router.

    Attributes:
        prefix (str): The prefix for the router.
        routes (List[Route]): The list of routes for the router.
        tags (List[str]): The tags for the router.
    """

    prefix: Annotated[str, Field(description="The prefix for the router")]
    routes: Annotated[List[Route], Field(description="The list of routes for the router")]
    tags: Annotated[List[str], Field(description="The tags for the router")]


class Router:
    def __init__(self, crud: CRUD, resource_name: str, models: Models) -> None:
        self.crud = crud
        self.resource_name = resource_name
        self.models = models

    @staticmethod
    def _replace_type_hint(original_func: Callable, type_name: str, new_type: type) -> Callable:
        if original_func.__annotations__ and type_name in original_func.__annotations__:
            original_func.__annotations__[type_name] = new_type
        return original_func

    @staticmethod
    def _wrapper_endpoint(
        original_func: Callable[..., Any],
        before_func: Callable[..., Any] = lambda *args, **kwargs: None,
        after_func: Callable[..., Any] = lambda *args, **kwargs: None,
    ) -> Callable[..., Any]:
        @wraps(original_func)
        async def wrapper(*args, **kwargs):
            before_func(*args, **kwargs)
            result = await original_func(*args, **kwargs)
            after_func(*args, **kwargs)
            return result

        return wrapper

    @property
    def _routes(self) -> list[Route]:
        create_endpoint = self._wrapper_endpoint(
            self._replace_type_hint(self.crud.create, "resource", self.models.create_model)
        )
        read_endpoint = self._wrapper_endpoint(self.crud.read)
        update_endpoint = self._wrapper_endpoint(
            self._replace_type_hint(self.crud.update, "resource", self.models.update_model)
        )
        delete_endpoint = self._wrapper_endpoint(self.crud.delete)
        read_many_endpoint = self._wrapper_endpoint(self.crud.read_many)
        return [
            Route(**route)
            for route in [
                {
                    "path": "/",
                    "endpoint": create_endpoint,
                    "response_model": self.models.response_model,
                    "methods": ["POST"],
                    "status_code": 201,
                },
                {
                    "path": "/{resource_id}/",
                    "endpoint": read_endpoint,
                    "response_model": self.models.response_model,
                    "methods": ["GET"],
                },
                {
                    "path": "/{resource_id}/",
                    "endpoint": update_endpoint,
                    "response_model": self.models.response_model,
                    "methods": ["PUT"],
                },
                {
                    "path": "/{resource_id}/",
                    "endpoint": update_endpoint,
                    "response_model": self.models.response_model,
                    "methods": ["PATCH"],
                    "name": "Update partial",
                },
                {
                    "path": "/{resource_id}/",
                    "endpoint": delete_endpoint,
                    "response_model": None,
                    "methods": ["DELETE"],
                    "status_code": 204,
                },
                {
                    "path": "/",
                    "endpoint": read_many_endpoint,
                    "response_model": list[self.models.response_model],
                    "methods": ["GET"],
                },
            ]
        ]

    @property
    def api_router(self) -> APIRouter:
        router = APIRouter(prefix=f"/{self.resource_name}", tags=[self.resource_name])
        for route in self._routes:
            router.add_api_route(
                path=route.path,
                endpoint=route.endpoint,
                response_model=route.response_model,
                methods=route.methods,  # type: ignore
                status_code=route.status_code,
                dependencies=route.dependencies,
            )
        return router
