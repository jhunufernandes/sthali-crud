"""{...}."""
from typing import Annotated
from uuid import UUID, uuid4

from fastapi import Depends, HTTPException, Request, status
from pydantic import ValidationError
from pydantic_core import ErrorDetails

from sthali_db import DB, Models, PaginateParameters
from sthali_db.models import Base, BaseWithId

ResponseModel = BaseWithId


class CRUDException(HTTPException):
    def __init__(
        self,
        detail: str | list[ErrorDetails],
        status_code: int = status.HTTP_422_UNPROCESSABLE_ENTITY,
    ) -> None:
        super().__init__(status_code, detail)


class CRUD:
    def __init__(self, db: DB, models: Models) -> None:
        self.db = db
        self.models = models

    @property
    def response_model(self) -> type[ResponseModel]:
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
        """Create a new resource.

        Args:
            resource (Base): The resource object to be created.

        Returns:
            ResponseModel: The response model containing the result of the operation.
        """
        resource_id = uuid4()
        resource_obj = resource.model_dump()
        result = await self.db.insert_one(resource_id=resource_id, resource_obj=resource_obj)
        return self._handle_result(result)

    async def read(self, resource_id: UUID) -> ResponseModel:
        """Retrieves a resource from the database based on the given resource ID.

        Args:
            resource_id (UUID): The ID of the resource to retrieve.

        Returns:
            ResponseModel: The retrieved resource.

        """
        result = await self.db.select_one(resource_id=resource_id)
        return self._handle_result(result)

    async def update(self, request: Request, resource_id: UUID, resource: Base) -> ResponseModel:
        """Update a resource in the database.

        Args:
            request (Request): The FastAPI request object.
            resource_id (UUID): The ID of the resource to update.
            resource (Base): The resource object containing the updated data.

        Returns:
            ResponseModel: The response model containing the result of the update operation.
        """
        partial = request.method == "PATCH"
        resource_obj = resource.model_dump(exclude_unset=partial)
        result = await self.db.update_one(resource_id=resource_id, resource_obj=resource_obj, partial=partial)
        return self._handle_result(result)

    async def delete(self, resource_id: UUID) -> None:
        """Deletes a resource with the given resource_id.

        Args:
            resource_id (UUID): The ID of the resource to delete.

        Raises:
            CRUDException: If the deletion fails.

        Returns:
            None: Indicates successful deletion.
        """
        result = await self.db.delete_one(resource_id=resource_id)
        try:
            assert result is None, "Result is not none"
        except AssertionError as _exception:
            raise CRUDException(repr(_exception), status.HTTP_500_INTERNAL_SERVER_ERROR) from _exception
        return result

    async def read_many(self, paginate_parameters: Annotated[dict, Depends(PaginateParameters)]) -> list[ResponseModel]:
        """Retrieves multiple records from the database based on pagination parameters.

        Args:
            paginate_parameters: Pagination parameters for selecting multiple records. The `paginate` parameter should containing
                the following args:
                - `page` (int): The page number to retrieve.
                - `limit` (int): The maximum number of records to retrieve per page.

        Returns:
            list[ResponseModel]: A list of response models representing the retrieved records.
        """
        result = await self.db.select_many(paginate_parameters)
        return self._handle_list(result)
