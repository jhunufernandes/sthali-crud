"""Methods for CRUD.
"""
from typing import Callable
from uuid import UUID
from fastapi import HTTPException
from pydantic import ValidationError
from .db import DB
from .helpers import ModelClass
from .schema import Base as Model
from .types import EmptyModel


class CRUD(ModelClass):
    """CRUD main class.
    """
    _db: DB
    # _deconstruct: Callable = lambda id=None, **rest: (id, rest)

    class CRUDException(HTTPException):
        """CRUD Exception.

        Args:
            HTTPException (Exception): FastAPI base Exception.
        """
        detail: str
        status_code: int

        def __init__(self, detail: str, status_code: int = 400) -> None:
            self.detail = detail
            self.status_code = status_code
            super().__init__(status_code, detail)

    def __init__(self, db: DB, model: Model) -> None:
        self._db = db
        self._model = model

    def _handle_crud_exception(self, exception: DB.DBException) -> None:
        """Handle CRUD Exception.

        Args:
            exception (DB.DBException): Custom DB Exception.

        Raises:
            self.CRUDException: Custom CRUD Exception.
        """
        raise self.CRUDException(repr(exception)) from exception

    async def _perform_crud(self, operation: Callable, resource: Model, validate: bool = True) -> Model | None:
        """Perform CRUD.

        Args:
            operation (Callable): DB function.
            resource_id (int, optional): Identifier from model. Defaults to None.
            resource (Model, optional): Model payload. Defaults to None.

        Returns:
            Model | None: Model payload or none.
        """
        try:
            resource_id = resource.id
            resource_obj = resource.model_dump()
            result = operation(resource_id=resource_id, resource_obj=resource_obj)
            if validate:
                result = self.model(**result)
            return result
        except DB.DBException as exception:
            self._handle_crud_exception(exception)
        except ValidationError as exception:
            raise self.CRUDException(detail=exception.errors(), status_code=422) from exception

    async def _upsert(self, resource: Model) -> Model:
        return await self._perform_crud(self._db.upsert, resource=resource)

    async def create(self, resource: Model) -> Model:
        return await self._upsert(resource=resource)

    async def read(self, resource_id: int) -> Model:
        return await self._perform_crud(self._db.read, resource_id=resource_id)

    async def update(self, resource: Model) -> Model:
        breakpoint()
        resource_id, resource_obj = (lambda id=None, **rest: (id, rest))(**resource.model_dump())
        resource_obj = self.model(**resource_obj)
        try:
            assert resource_id
        except AssertionError as exception:
            breakpoint()
            raise self.CRUDException(detail='id', status_code=422) from exception
        return await self._upsert(resource_id=resource_id, resource_obj=resource_obj)

    # async def delete(self, resource_id: int) -> None:
    #     return await self._perform_crud(self._db.delete, resource_id=resource_id, validate=False)
