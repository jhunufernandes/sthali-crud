from uuid import UUID, uuid4

from fastapi import Depends, HTTPException, status
from pydantic import ValidationError
from pydantic_core import ErrorDetails

from sthali_db import DBEngine, filter_parameters

from .models import Base, Models

ResponseModel = Base


class CRUDException(HTTPException):
    def __init__(
        self,
        detail: str | list[ErrorDetails],
        status_code: int = status.HTTP_422_UNPROCESSABLE_ENTITY,
    ) -> None:
        super().__init__(status_code, detail)


class CRUD:
    db: DBEngine
    models: Models

    def __init__(self, db: DBEngine, models: Models) -> None:
        self.db = db
        self.models = models

    @property
    def response_model(self) -> type[Base]:
        return self.models.response_model

    def _handle_list(self, result: list[dict]) -> list[ResponseModel]:
        errors = []
        response_result = []

        for r in result:
            try:
                response_result.append(self._handle_result(r))
            except CRUDException as exception:
                errors.append(exception.detail)

        try:
            assert not errors
        except AssertionError as exception:
            raise CRUDException(errors) from exception

        return response_result

    def _handle_result(self, result: dict | None) -> ResponseModel:
        try:
            assert result, "Not found"
            response_result = self.response_model(**result)
        except AssertionError as exception:
            raise CRUDException(exception.args[0], status.HTTP_404_NOT_FOUND) from exception
        except ValidationError as exception:
            raise CRUDException(exception.errors()) from exception

        return response_result

    async def create(self, resource: Base) -> ResponseModel:
        resource_id = uuid4()
        resource_obj = resource.model_dump()
        result = await self.db.insert_one(resource_id=resource_id, resource_obj=resource_obj)
        return self._handle_result(result)

    async def read(self, resource_id: UUID) -> ResponseModel:
        result = await self.db.select_one(resource_id=resource_id)
        return self._handle_result(result)

    async def update(self, resource: Base, resource_id: UUID | None = None) -> ResponseModel:
        _resource_id, resource_obj = (lambda id=None, **rest: (id, rest))(**resource.model_dump())
        try:
            assert any([_resource_id, resource_id]), "None id is defined"
            if all([_resource_id, resource_id]):
                assert _resource_id == resource_id, "Ids cant match"
        except AssertionError as _exception:
            raise CRUDException(repr(_exception), 404) from _exception

        result = await self.db.update_one(resource_id=(_resource_id or resource_id), resource_obj=resource_obj)
        return self._handle_result(result)

    async def delete(self, resource_id: UUID) -> None:
        result = await self.db.delete_one(resource_id=resource_id)
        try:
            assert result is None, "Result is not none"
        except AssertionError as _exception:
            raise CRUDException(repr(_exception), status.HTTP_500_INTERNAL_SERVER_ERROR) from _exception

        return result

    async def read_many(self, paginate: dict = Depends(filter_parameters)) -> list[ResponseModel]:
        result = await self.db.select_many(**paginate)
        return self._handle_list(result)
