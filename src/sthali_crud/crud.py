"""Methods for CRUD.
"""
from typing import Callable
from fastapi import HTTPException
from pydantic import BaseModel
from .db import DB


class CRUD:
    """CRUD main class.
    """
    _db: DB
    _model: type[BaseModel]

    class CRUDException(HTTPException):
        """CRUD Exception.

        Args:
            HTTPException (Exception): FastAPI base Exception.
        """
        def __init__(self, detail: str, status_code: int = 400) -> None:
            self.detail = detail
            self.status_code = status_code
            super().__init__(status_code, detail)

    def __init__(self, db: DB, model: type[BaseModel]) -> None:
        self._db = db
        self._model = model

    def _handle_crud_exception(self, exception: DB.DBException) -> None:
        """Handle CRUD Exception.

        Args:
            exception (DB.DBException): Custom DB Exception.

        Raises:
            self.CRUDException: Custom CRUD Exception.
        """
        raise self.CRUDException(detail=repr(exception), status_code=400) from exception

    async def _perform_crud(self,
                            operation: Callable,
                            resource_id: int = None,
                            resource: type[BaseModel] = None) -> type[BaseModel] | None:
        """Perform CRUD.

        Args:
            operation (Callable): DB function.
            resource_id (int, optional): Identifier from model. Defaults to None.
            resource (type[BaseModel], optional): Model payload. Defaults to None.

        Returns:
            type[BaseModel] | None: Model payload or none.
        """
        try:
            return operation(resource_id, resource)
        except DB.DBException as exception:
            self._handle_crud_exception(exception)

    async def create(self, resource: type[BaseModel]) -> type[BaseModel]:
        return await self._perform_crud(self._db.create, resource=resource)

    async def read(self, resource_id: int) -> type[BaseModel]:
        return await self._perform_crud(self._db.read, resource_id=resource_id)

    async def update(self, resource_id: int, resource: type[BaseModel]) -> type[BaseModel]:
        return await self._perform_crud(self._db.update, resource_id=resource_id, resource=resource)

    async def delete(self, resource_id: int) -> None:
        return await self._perform_crud(self._db.delete, resource_id=resource_id)
