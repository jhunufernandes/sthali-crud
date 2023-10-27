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

    def _handle_result(self, result: dict | None):
        try:
            assert result, "not found"
            _response_result = self.response_model(**result)
        except AssertionError as exception:
            raise HTTPException(status.HTTP_404_NOT_FOUND, exception.args[0]) from exception
        except ValidationError as exception:
            raise CRUDException(exception.errors()) from exception
        except Exception as exception:
            raise CRUDException(repr(exception)) from exception
        else:
            return _response_result

    async def _perform_crud(
        self,
        operation: Callable,
        resource_id: UUID | None = None,
        resource_obj: dict | None = None,
    ) -> dict | None:
        return await operation(resource_id=resource_id, resource_obj=resource_obj)

    async def create(self, resource: BaseModel):
        """create route.

        Args:
            resource (type[CreateModel]): Create model.

        Returns:
            ResponseModel: Resource response model.
        """
        _resource_id = uuid4()
        _resource_obj = resource.model_dump()
        _result = await self._perform_crud(
            self.db.create, resource_id=_resource_id, resource_obj=_resource_obj
        )
        return self._handle_result(_result)

    async def read(self, resource_id: UUID):
        """read route.

        Args:
            resource_id (UUID): Resource id.

        Returns:
            ResponseModel: Resource response model.
        """
        _result = await self._perform_crud(self.db.read, resource_id=resource_id)
        return self._handle_result(_result)

    async def update(self, resource: BaseModel, resource_id: UUID | None = None):
        """update route. Validate id on query or body.

        Args:
            resource (type[UpdateModel]): Update model.
            resource_id (UUID | None, optional): Resource id. Defaults to None.

        Raises:
            CRUDException: AssertionError when id is invalid.

        Returns:
            ResponseModel: Resource response model.
        """
        _resource_id, _resource_obj = (lambda id=None, **rest: (id, rest))(
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
        _resource_id = _resource_id or resource_id
        _result = await self._perform_crud(
            self.db.update, resource_id=_resource_id, resource_obj=_resource_obj
        )
        return self._handle_result(_result)

    async def delete(self, resource_id: UUID) -> None:
        """delete route.

        Args:
            resource_id (UUID): Resource id.

        Raises:
            CRUDException: AssertionError when result is not none.

        Returns:
            None: None is returned.
        """
        _result = await self._perform_crud(self.db.delete, resource_id=resource_id)
        try:
            assert _result is None, "result is not none"
        except AssertionError as _exception:
            raise CRUDException(repr(_exception)) from _exception
        else:
            return _result
