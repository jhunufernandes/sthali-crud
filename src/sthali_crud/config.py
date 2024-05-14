import contextlib
import functools
import json
import logging
import typing

import fastapi
import yaml

from .crud import CRUD
from .models import Models
from .types import RouteConfiguration, RouterConfiguration


class Types:
    any = typing.Any
    none = None
    bool = bool
    true = True
    false = False
    str = str
    int = int
    float = float
    list = list
    dict = dict


class ConfigException(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)


def config_router(crud: CRUD, name: str, models: Models) -> RouterConfiguration:
    create_endpoint = wrapper_endpoint(replace_type_hint(crud.create, "resource", models.create_model))
    read_endpoint = wrapper_endpoint(crud.read)
    update_endpoint = wrapper_endpoint(replace_type_hint(crud.update, "resource", models.update_model))
    delete_endpoint = wrapper_endpoint(crud.delete)
    read_many_endpoint = wrapper_endpoint(crud.read_many)
    return RouterConfiguration(
        prefix=f"/{name}",
        routes=[
            RouteConfiguration(
                path="/",
                endpoint=create_endpoint,
                response_model=models.response_model,
                methods=["POST"],
                status_code=201,
            ),
            RouteConfiguration(
                path="/{resource_id}/",
                endpoint=read_endpoint,
                response_model=models.response_model,
                methods=["GET"],
            ),
            RouteConfiguration(
                path="/{resource_id}/",
                endpoint=update_endpoint,
                response_model=models.response_model,
                methods=["PUT"],
            ),
            RouteConfiguration(
                path="/{resource_id}/",
                endpoint=update_endpoint,
                response_model=models.response_model,
                methods=["PATCH"],
                # name="Update partial",
            ),
            RouteConfiguration(
                path="/{resource_id}/",
                endpoint=delete_endpoint,
                response_model=None,
                methods=["DELETE"],
                status_code=204,
            ),
            RouteConfiguration(
                path="/",
                endpoint=read_many_endpoint,
                response_model=list[models.response_model],
                methods=["GET"],
            ),
        ],
        tags=[name],
    )


@contextlib.asynccontextmanager
async def default_lifespan(app: fastapi.FastAPI):
    logging.info("Startup SthaliCRUD")
    yield
    logging.info("Shutdown SthaliCRUD")


def get_type(type_str: str) -> typing.Any:
    type_str = type_str.strip().lower()
    try:
        return getattr(Types, type_str)
    except AttributeError as exception:
        raise ConfigException("Invalid type") from exception


def load_and_parse_spec_file(spec_file_path: str) -> dict:
    spec_dict = load_spec_file(spec_file_path)

    for resource in spec_dict["resources"]:
        for field in resource["fields"]:
            if isinstance(field["type"], str):
                field["type"] = get_type(field["type"])
            elif isinstance(field["type"], list):
                types_list = tuple(get_type(type) for type in field["type"])
                field["type"] = typing.Union[types_list]  # type: ignore
            else:
                raise ConfigException("Invalid field type")
            if "has_default" in field:
                field["has_default"] = get_type(field["has_default"])
    return spec_dict


def load_spec_file(spec_file_path: str) -> dict:
    spec_file_extension = spec_file_path.split(".")[-1]
    if spec_file_extension not in ("yaml", "yml", "json"):
        raise ConfigException("Invalid file extension")

    with open(spec_file_path, "r", encoding="utf-8") as spec_file:
        return json.load(spec_file) if spec_file_extension == "json" else yaml.safe_load(spec_file)


def replace_type_hint(original_func: typing.Callable, type_name: str, new_type: type) -> typing.Callable:
    if original_func.__annotations__ and type_name in original_func.__annotations__:
        original_func.__annotations__[type_name] = new_type
    return original_func


def wrapper_endpoint(
    original_func: typing.Callable[..., typing.Any],
    before_func: typing.Callable[..., typing.Any] = lambda *args, **kwargs: None,
    after_func: typing.Callable[..., typing.Any] = lambda *args, **kwargs: None,
) -> typing.Callable[..., typing.Any]:
    @functools.wraps(original_func)
    async def wrapper(*args, **kwargs):
        before_func(*args, **kwargs)
        result = await original_func(*args, **kwargs)
        after_func(*args, **kwargs)
        return result

    return wrapper
