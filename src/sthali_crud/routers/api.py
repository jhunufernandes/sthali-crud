"""{...}."""

from typing import Annotated
from uuid import UUID, uuid4

from fastapi import APIRouter, Depends, HTTPException, Request, status
from sqlalchemy import select

from ..database import DbSession, ModelType, SchemaType
from ..dependencies import PaginateParameters
from . import Base, replace_type_hint


class API(Base):
    """{...}."""

    def __init__(self, *args, **kwargs) -> None:
        """{...}."""
        super().__init__(*args, **kwargs)

    async def api_create(self, db: DbSession, resource: SchemaType) -> SchemaType:
        """Create a new resource.

        Args:
            resource (SchemaType): The resource object to be created.

        Returns:
            SchemaType: The response model containing the result of the operation.
        """
        resource_id = uuid4()
        resource_obj = resource.model_dump()
        resource = self.model(**resource_obj, id=resource_id)
        db.add(resource)
        await db.commit()
        return self._handle_result(resource)

    async def api_read(self, db: DbSession, resource_id: UUID) -> SchemaType:
        """Retrieves a resource from the database based on the given resource ID.

        Args:
            resource_id (UUID): The ID of the resource to retrieve.

        Returns:
            SchemaType: The retrieved resource.

        """
        result = await db.get(self.model, resource_id)
        return self._handle_result(result)

    async def api_update(self, request: Request, db: DbSession, resource_id: UUID, resource: SchemaType) -> SchemaType:
        """Update a resource in the database.

        Args:
            request (Request): The FastAPI request object.
            resource_id (UUID): The ID of the resource to update.
            resource (SchemaType): The resource object containing the updated data.

        Returns:
            SchemaType: The response model containing the result of the update operation.
        """
        result = await db.get(self.model, resource_id)
        if not result:
            raise HTTPException(status.HTTP_404_NOT_FOUND, "Record not found")

        partial = request.method == "PATCH"
        resource_obj = resource.model_dump(exclude_unset=partial)

        for key, value in resource_obj.items():
            setattr(result, key, value)
        await db.commit()
        await db.refresh(result)
        return self._handle_result(result)

    async def api_delete(self, db: DbSession, resource_id: UUID) -> None:
        """Deletes a resource with the given resource_id.

        Args:
            resource_id (UUID): The ID of the resource to delete.

        Raises:
            CRUDException: If the deletion fails.

        Returns:
            None: Indicates successful deletion.
        """
        await db.delete(resource_id)
        await db.commit()

    async def api_read_many(
        self,
        db: DbSession,
        paginate_parameters: Annotated[
            PaginateParameters,
            Depends(PaginateParameters),
        ],
    ) -> list[SchemaType]:
        """Retrieves multiple records from the database based on pagination parameters.

        Args:
            paginate_parameters: Pagination parameters for selecting multiple records. The `paginate` parameter should
                containing the following args:
                - `page` (int): The page number to retrieve.
                - `limit` (int): The maximum number of records to retrieve per page.

        Returns:
            list[SchemaType]: A list of response models representing the retrieved records.
        """
        query = await db.execute(select(self.model))
        result: list[ModelType] = query.scalars().all()  # type: ignore
        return self._handle_list_result(result)

    @property
    def api_router(self) -> APIRouter:
        router = APIRouter(prefix=f"/{self.resource_name}", tags=[self.resource_name])
        router.add_api_route(
            "/",
            replace_type_hint(self.api_create, "resource", self.create_schema),
            response_model=self.read_schema,
            methods=["POST"],
            status_code=201,
        )
        router.add_api_route("/{resource_id}/", self.api_read, response_model=self.read_schema, methods=["GET"])
        router.add_api_route(
            "/{resource_id}/",
            replace_type_hint(self.api_update, "resource", self.update_schema),
            response_model=self.read_schema,
            methods=["PUT"],
        )
        router.add_api_route(
            "/{resource_id}/",
            replace_type_hint(self.api_update, "resource", self.update_schema),
            response_model=self.read_schema,
            methods=["PATCH"],
        )
        router.add_api_route(
            "/{resource_id}/",
            self.api_delete,
            response_model=None,
            methods=["DELETE"],
            status_code=204,
        )
        router.add_api_route("/", self.api_read_many, response_model=list[self.read_schema], methods=["GET"])  # type: ignore
        return router
