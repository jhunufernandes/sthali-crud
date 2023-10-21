"""Methods for CRUD.
"""
from typing import Any, Callable, Literal
from uuid import UUID
from fastapi import HTTPException
from pydantic import BaseModel, ValidationError
from .db import DB
from .models import Models, CreateInputModel, UpdateInputModel, UpsertInputModel
from .schema import Schema


class CRUD:
    _db: DB
    _schema: Schema
    # _deconstruct: Callable = lambda id=None, **rest: (id, rest)

    class CRUDException(HTTPException):
        """CRUD Exception.

        Args:
            HTTPException (Exception): FastAPI Model Exception.
        """
        detail: str
        status_code: int

        def __init__(self, detail: str, status_code: int = 400) -> None:
            self.detail = detail
            self.status_code = status_code
            super().__init__(status_code, detail)

    def __init__(self, db: DB, schema: Schema) -> None:
        self._db = db
        self._schema = schema

    @property
    def schema(self) -> Schema:
        return self._schema

    def _handle_crud_exception(self, exception: DB.DBException) -> None:
        """Handle CRUD Exception.

        Args:
            exception (DB.DBException): Custom DB Exception.

        Raises:
            self.CRUDException: Custom CRUD Exception.
        """
        raise self.CRUDException(repr(exception)) from exception

    async def _perform_crud(
            self,
            operation: Callable,
            resource_obj: Any | None = None,
            resource_id: UUID | None = None) -> Any | None:
        result = operation(resource_id=resource_id, resource_obj=resource_obj)
        breakpoint()
        return result

        # return None
        # try:
        #     resource_id = resource.id
        #     resource_obj = resource.model_dump()
        # except DB.DBException as exception:
        # self._handle_crud_exception(exception)
        # except ValidationError as exception:
        #     raise self.CRUDException(detail=exception.errors(), status_code=422) from exception

    async def _upsert(self, resource: BaseModel, resource_id: UUID | None = None) -> Any:
        result = await self._perform_crud(self._db.upsert, resource_id=resource_id, resource_obj=resource.model_dump())
        breakpoint()
        try:
            assert result
            # return self.schema.create_resource_model(**result.model_dump())
            return {}
        except AssertionError as _exception:
            raise self.CRUDException(detail='id', status_code=422) from _exception

    async def create(self, resource: CreateInputModel) -> Any:
        breakpoint()
        return resource
        # return await self._upsert(resource=resource)

    # async def read(self, resource_id: int) -> Any:
    #     return await self._perform_crud(self._db.read, resource_id=resource_id)

    # async def update(self, resource: Any) -> Any:
    #     breakpoint()
    #     resource_id, resource_obj = (lambda id=None, **rest: (id, rest))(**resource.model_dump())
    #     # resource_obj = self.model(**resource_obj)
    #     try:
    #         assert resource_id
    #     except AssertionError as exception:
    #         breakpoint()
    #         raise self.CRUDException(detail='id', status_code=422) from exception
    #     return await self._upsert(resource_id=resource_id, resource_obj=resource_obj)

    # async def delete(self, resource_id: UUID) -> None:
    #     result = await self._perform_crud(self._db.delete, resource_id=resource_id)
    #     try:
    #         assert result is None
    #     except AssertionError as _exception:
    #         breakpoint()
    #         raise self.CRUDException(detail='something wrong', status_code=422) from _exception
    #     else:
    #         return None
