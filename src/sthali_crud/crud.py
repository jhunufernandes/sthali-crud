from typing import Callable
from uuid import UUID, uuid4

from fastapi import status
from pydantic import ValidationError
from pydantic_core import ErrorDetails

from .db import DB
from .exceptions import SthaliCRUDException
from .models import CreateModel, Models, ResponseModel, UpdateModel


class CRUD:
    """CRUD main class.

    Raises:
        self.CRUDException: AssertionError when result is invalid.
        self.CRUDException: ValidationError when result model is invalid.
        self.CRUDException: Exception for general exceptions.
    """

    _db: DB
    _models: Models

    class CRUDException(SthaliCRUDException):
        """CRUDException.

        Args:
            SthaliCRUDException (Exception): FastAPI Model Exception.
        """

        def __init__(
            self,
            detail: str | list[ErrorDetails],
            status_code: int = status.HTTP_422_UNPROCESSABLE_ENTITY,
        ) -> None:
            super().__init__(detail, status_code)

    def __init__(self, db: DB, models: Models) -> None:
        self._db = db
        self._models = models

    @property
    def response_model(self) -> type[ResponseModel]:
        return self._models.response_model

    def _handle_result(self, result: ResponseModel | None) -> ResponseModel:
        try:
            assert result, "result is none"
            _response_result = self.response_model(**result)
        except AssertionError as _exception:
            raise self.CRUDException(repr(_exception)) from _exception
        except ValidationError as _exception:
            raise self.CRUDException(_exception.errors()) from _exception
        except Exception as _exception:
            raise self.CRUDException(repr(_exception)) from _exception
        else:
            return _response_result

    async def _perform_crud(
        self,
        operation: Callable,
        resource_id: UUID | None = None,
        resource_obj: dict | None = None,
    ) -> ResponseModel | None:
        return await operation(resource_id=resource_id, resource_obj=resource_obj)

    async def create(self, resource: type[CreateModel]) -> ResponseModel:
        """create route.

        Args:
            resource (type[CreateModel]): Create model.

        Returns:
            ResponseModel: Resource response model.
        """
        _resource_id = uuid4()
        _resource_obj = resource.model_dump()
        _result = await self._perform_crud(
            self._db.create, resource_id=_resource_id, resource_obj=_resource_obj
        )
        return self._handle_result(_result)

    async def read(self, resource_id: UUID) -> ResponseModel:
        """read route.

        Args:
            resource_id (UUID): Resource id.

        Returns:
            ResponseModel: Resource response model.
        """
        _result = await self._perform_crud(self._db.read, resource_id=resource_id)
        return self._handle_result(_result)

    async def update(
        self, resource: type[UpdateModel], resource_id: UUID | None = None
    ) -> ResponseModel:
        """update route. Validate id on query or body.

        Args:
            resource (type[UpdateModel]): Update model.
            resource_id (UUID | None, optional): Resource id. Defaults to None.

        Raises:
            self.CRUDException: AssertionError when id is invalid.

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
            raise self.CRUDException(repr(_exception), 404) from _exception
        _resource_id = _resource_id or resource_id
        _result = await self._perform_crud(
            self._db.update, resource_id=_resource_id, resource_obj=_resource_obj
        )
        return self._handle_result(_result)

    async def delete(self, resource_id: UUID) -> None:
        """delete route.

        Args:
            resource_id (UUID): Resource id.

        Raises:
            self.CRUDException: AssertionError when result is not none.

        Returns:
            None: None is returned.
        """
        _result = await self._perform_crud(self._db.delete, resource_id=resource_id)
        try:
            assert _result is None, "result is not none"
        except AssertionError as _exception:
            raise self.CRUDException(repr(_exception)) from _exception
        else:
            return _result
