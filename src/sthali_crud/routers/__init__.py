"""Abstract base router class for Sthali CRUD route handlers."""

from collections.abc import AsyncGenerator, Callable
from typing import ClassVar

from fastapi import APIRouter, HTTPException, status
from pydantic import ValidationError
from sthali_db import DBSession, ModelType, SchemaType


class Base:
    """Abstract base class for Sthali router implementations."""

    prefix: ClassVar[str | None] = None

    def __init__(
        self,
        db_session: Callable[[], AsyncGenerator[DBSession, None]],
        model: ModelType,
        create_schema: SchemaType,
        read_schema: SchemaType,
        update_schema: SchemaType,
    ) -> None:
        """Store the session factory and schema references for CRUD operations.

        Args:
            db_session: Async session factory used as a FastAPI dependency.
            model: The SQLAlchemy model class for this router.
            create_schema: Pydantic schema for create operations.
            read_schema: Pydantic schema for read responses.
            update_schema: Pydantic schema for update operations.
        """
        self.db_session = db_session
        self.model = model
        self.read_schema = read_schema
        self.create_schema = create_schema
        self.update_schema = update_schema

    @property
    def api_router(self) -> APIRouter:
        """Return the configured FastAPI APIRouter for this handler."""
        raise NotImplementedError

    @property
    def resource_name(self) -> str:
        """Return the table name of the model used as the URL resource segment."""
        return self.model.__tablename__

    def handle_result(self, result: ModelType | None) -> SchemaType:
        """Validate a single ORM result and return the read schema instance.

        Args:
            result: The ORM object returned from the database query.

        Returns:
            The validated schema instance.

        Raises:
            HTTPException: 404 if result is None; 422 if schema validation fails.
        """
        if not result:
            raise HTTPException(status.HTTP_404_NOT_FOUND, "Resource not found")
        try:
            schema: SchemaType = self.read_schema  # type: ignore[assignment]
            return schema.model_validate(result)
        except ValidationError as e:
            raise HTTPException(status.HTTP_422_UNPROCESSABLE_ENTITY, e.errors()) from e

    def handle_list_result(self, result: list[ModelType]) -> list[SchemaType]:
        """Validate a list of ORM results and return validated schema instances.

        Args:
            result: List of ORM objects from the database query.

        Returns:
            A list of validated schema instances.

        Raises:
            HTTPException: 400 if any result fails validation.
        """
        errors: list[HTTPException] = []
        response_result: list[SchemaType] = []

        for r in result:
            try:
                response_result.append(self.handle_result(r))
            except HTTPException as e:  # noqa: PERF203
                errors.append(e)
        if errors:
            raise HTTPException(status.HTTP_400_BAD_REQUEST, [e.detail for e in errors])
        return response_result
