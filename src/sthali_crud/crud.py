from typing import Callable
from uuid import UUID, uuid4

from fastapi import HTTPException, status
from pydantic import BaseModel, ValidationError
from pydantic_core import ErrorDetails

from .db import DB
from .models import Models


class CRUDException(HTTPException):
    def __init__(
        self,
        detail: str | list[ErrorDetails],
        status_code: int = status.HTTP_422_UNPROCESSABLE_ENTITY,
    ) -> None:
        super().__init__(status_code, detail)


class CRUD:
    db: DB
    models: Models

    def __init__(self, db: DB, models: Models) -> None:
        self.db = db
        self.models = models

    @property
    def response_model(self):
        return self.models.response_model

    def _handle_list(self, result: list):
        errors = []
        response_result = []

        for r in result:
            try:
                assert r, "not found"
                response_result.append(self.response_model(**r))
            except AssertionError as exception:
                errors.append(exception.args[0])
            except ValidationError as exception:
                errors.append(exception.errors())
            except Exception as exception:
                breakpoint()
                errors.append(repr(exception))

        try:
            assert not errors
        except AssertionError as exception:
            raise CRUDException(errors) from exception

        return response_result

    def _handle_result(self, result: dict | list | None):
        if isinstance(result, list):
            return self._handle_list(result)

        try:
            assert result, "not found"
            response_result = self.response_model(**result)
        except AssertionError as exception:
            raise HTTPException(
                status.HTTP_404_NOT_FOUND, exception.args[0]
            ) from exception
        except ValidationError as exception:
            raise CRUDException(exception.errors()) from exception
        except Exception as exception:
            raise CRUDException(repr(exception)) from exception

        return response_result

    async def _perform_crud(
        self,
        operation: Callable,
        resource_id: UUID | None = None,
        resource_obj: dict | None = None,
    ) -> dict | None:
        return await operation(resource_id=resource_id, resource_obj=resource_obj)

    async def create(self, resource: BaseModel):
        resource_id = uuid4()
        resource_obj = resource.model_dump()
        result = await self._perform_crud(
            self.db.create, resource_id=resource_id, resource_obj=resource_obj
        )
        return self._handle_result(result)

    async def read(self, resource_id: UUID):
        result = await self._perform_crud(self.db.read, resource_id=resource_id)
        return self._handle_result(result)

    async def update(self, resource: BaseModel, resource_id: UUID | None = None):
        _resource_id, resource_obj = (lambda id=None, **rest: (id, rest))(
            **resource.model_dump()
        )
        try:
            assert any([_resource_id, resource_id]), "None id is defined"
            assert (
                _resource_id == resource_id
                if all([_resource_id, resource_id])
                else _resource_id or resource_id
            ), "Ids cant match"
        except AssertionError as _exception:
            raise CRUDException(repr(_exception), 404) from _exception

        resource_id = _resource_id or resource_id
        result = await self._perform_crud(
            self.db.update, resource_id=resource_id, resource_obj=resource_obj
        )
        return self._handle_result(result)

    async def delete(self, resource_id: UUID) -> None:
        result = await self._perform_crud(self.db.delete, resource_id=resource_id)
        try:
            assert result is None, "result is not none"
        except AssertionError as _exception:
            raise CRUDException(repr(_exception)) from _exception

        return result

    async def read_all(self):
        result = await self._perform_crud(self.db.read_all)
        return self._handle_result(result)
