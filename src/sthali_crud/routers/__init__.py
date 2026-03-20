"""{...}."""

from fastapi import APIRouter, HTTPException, status
from pydantic import ValidationError
from sthali_db import DBSession, ModelType, SchemaType


class Base:
    """{...}."""

    prefix: str | None = None

    def __init__(
        self,
        db_session: DBSession,
        model: ModelType,
        create_schema: SchemaType,
        read_schema: SchemaType,
        update_schema: SchemaType,
    ) -> None:
        """{…}."""
        self.db_session = db_session
        self.model = model
        self.read_schema = read_schema
        self.create_schema = create_schema
        self.update_schema = update_schema

    @property
    def api_router(self) -> APIRouter:
        raise NotImplementedError

    @property
    def resource_name(self) -> str:
        """{...}."""
        return self.model.__tablename__

    def handle_result(self, result: ModelType | None) -> SchemaType:
        """{...}."""
        if not result:
            raise HTTPException(status.HTTP_404_NOT_FOUND, "Resource not found")
        try:
            schema: SchemaType = self.read_schema  # type: ignore
            return schema.model_validate(result)
        except ValidationError as e:
            raise HTTPException(status.HTTP_422_UNPROCESSABLE_ENTITY, e.errors()) from e

    def handle_list_result(self, result: list[ModelType]) -> list[SchemaType]:
        """{...}."""
        errors: list[HTTPException] = []
        response_result: list[SchemaType] = []

        for r in result:
            try:
                response_result.append(self.handle_result(r))
            except HTTPException as e:
                errors.append(e)
        if errors:
            raise HTTPException(status.HTTP_400_BAD_REQUEST, [e.detail for e in errors])
        return response_result
