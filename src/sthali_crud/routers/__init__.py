"""{...}."""

from collections.abc import Callable
from typing import Any

from fastapi import HTTPException, status
from fastapi.templating import Jinja2Templates
from pydantic import ValidationError

from ..database import ModelType, SchemaType


def replace_type_hint(
    original_func: Callable[..., Any],
    type_name: str,
    new_type: type,
) -> Callable[..., Any]:
    """{...}."""
    if original_func.__annotations__ and type_name in original_func.__annotations__:
        original_func.__annotations__[type_name] = new_type
    return original_func


def handle_result(schema: type[SchemaType], model: ModelType | None) -> SchemaType:
    """{...}."""
    if not model:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Record not found")
    try:
        return schema.model_validate(model)
    except ValidationError as e:
        raise HTTPException(status.HTTP_422_UNPROCESSABLE_ENTITY, e.errors()) from e


def handle_list_result(schema: type[SchemaType], result: list[ModelType]) -> list[SchemaType]:
    """{...}."""
    errors: list[HTTPException] = []
    response_result: list[SchemaType] = []

    for r in result:
        try:
            response_result.append(handle_result(schema, r))
        except HTTPException as e:
            errors.append(e)
    if errors:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, [e.detail for e in errors])
    return response_result


class Base:
    """{...}."""

    def __init__(
        self,
        model: ModelType,
        schema: type[SchemaType],
        create_schema: type[SchemaType] | None = None,
        update_schema: type[SchemaType] | None = None,
        templates: Jinja2Templates | None = None,
    ) -> None:
        """{...}."""
        self.model = model
        self.schema = schema
        self.create_schema = create_schema or schema
        self.update_schema = update_schema or schema
        self.templates = templates

    def _handle_result(self, result: ModelType | None) -> SchemaType:
        return handle_result(self.schema, result)  # type: ignore

    def _handle_list_result(self, result: list[ModelType]) -> list[SchemaType]:
        return handle_list_result(self.schema, result)  # type: ignore

    @property
    def resource_name(self) -> str:
        """{...}."""
        return self.model.__tablename__
