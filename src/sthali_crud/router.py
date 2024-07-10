import typing

import pydantic
import fastapi
import sthali_db

from .crud import CRUD


@pydantic.dataclasses.dataclass
class Route:
    """Route Configuration."""

    path: str
    endpoint: typing.Callable[..., typing.Any]
    response_model: typing.Any
    methods: list[typing.Literal["GET", "POST", "PUT", "PATCH", "DELETE"]]
    status_code: int = 200
    dependencies: list = pydantic.Field(default_factory=list)
    name: str | None = None


@pydantic.dataclasses.dataclass
class RouterConfiguration:
    """Router Configuration."""

    prefix: str
    routes: list[Route]
    tags: list[str]


class Router:
    def config(crud: CRUD, name: str, models: sthali_db.Models) -> RouterConfiguration:
        # create_endpoint = wrapper_endpoint(replace_type_hint(crud.create, "resource", models.create_model))
        # read_endpoint = wrapper_endpoint(crud.read)
        # update_endpoint = wrapper_endpoint(replace_type_hint(crud.update, "resource", models.update_model))
        # delete_endpoint = wrapper_endpoint(crud.delete)
        # read_many_endpoint = wrapper_endpoint(crud.read_many)
        return RouterConfiguration(
            prefix=f"/{name}",
            routes=[
                # RouteConfiguration(
                #     path="/",
                #     endpoint=create_endpoint,
                #     response_model=models.response_model,
                #     methods=["POST"],
                #     status_code=201,
                # ),
                # RouteConfiguration(
                #     path="/{resource_id}/",
                #     endpoint=read_endpoint,
                #     response_model=models.response_model,
                #     methods=["GET"],
                # ),
                # RouteConfiguration(
                #     path="/{resource_id}/",
                #     endpoint=update_endpoint,
                #     response_model=models.response_model,
                #     methods=["PUT"],
                # ),
                # RouteConfiguration(
                #     path="/{resource_id}/",
                #     endpoint=update_endpoint,
                #     response_model=models.response_model,
                #     methods=["PATCH"],
                #     # name="Update partial",
                # ),
                # RouteConfiguration(
                #     path="/{resource_id}/",
                #     endpoint=delete_endpoint,
                #     response_model=None,
                #     methods=["DELETE"],
                #     status_code=204,
                # ),
                # RouteConfiguration(
                #     path="/",
                #     endpoint=read_many_endpoint,
                #     response_model=list[models.response_model],
                #     methods=["GET"],
                # ),
            ],
            tags=[name],
        )

