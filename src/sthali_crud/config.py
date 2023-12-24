import logging
import json
from contextlib import asynccontextmanager
from yaml import safe_load
from typing import Any, Callable, Union

from fastapi import FastAPI

from .crud import CRUD
from .models import Models
from .types import RouteConfiguration, RouterConfiguration


class Types:
    any = Any
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


@asynccontextmanager
async def default_lifespan(app: FastAPI):
    logging.info("Startup SthaliCRUD")
    yield
    logging.info("Shutdown SthaliCRUD")


def replace_type_hint(original_func: Callable, type_name: str, new_type: type) -> Callable:
    if original_func.__annotations__ and type_name in original_func.__annotations__:
        original_func.__annotations__[type_name] = new_type
    return original_func


def config_router(crud: CRUD, name: str, models: Models) -> RouterConfiguration:
    return RouterConfiguration(
        prefix=f"/{name}",
        routes=[
            RouteConfiguration(
                path="/",
                endpoint=replace_type_hint(crud.create, "resource", models.create_model),
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
                endpoint=replace_type_hint(crud.update, "resource", models.update_model),
                response_model=models.response_model,
                methods=["PUT"],
            ),
            RouteConfiguration(
                path="/{resource_id}/",
                endpoint=replace_type_hint(crud.update, "resource", models.upsert_model),
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


def get_type(type_str: str) -> Any:
    type_str = type_str.strip().lower()
    try:
        return getattr(Types, type_str)
    except AttributeError as exception:
        raise ConfigException("Invalid type") from exception


def load_spec_file(spec_file_path: str) -> dict:
    spec_file_extension = spec_file_path.split(".")[-1]
    if spec_file_extension not in ("yaml", "yml", "json"):
        raise ConfigException("Invalid file extension")

    with open(spec_file_path, "r", encoding="utf-8") as spec_file:
        return json.load(spec_file) if spec_file_extension == "json" else safe_load(spec_file)


def load_and_parse_spec_file(spec_file_path: str) -> dict:
    spec_dict = load_spec_file(spec_file_path)

    for resource in spec_dict["resources"]:
        for field in resource["fields"]:
            if isinstance(field["type"], str):
                field["type"] = get_type(field["type"])
            elif isinstance(field["type"], list):
                types_list = tuple(get_type(type) for type in field["type"])
                field["type"] = Union[types_list]  # type: ignore
            else:
                raise ConfigException("Invalid field type")
            if "has_default" in field:
                field["has_default"] = get_type(field["has_default"])
    return spec_dict
