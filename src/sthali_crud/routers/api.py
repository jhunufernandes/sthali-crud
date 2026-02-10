"""{...}."""
from typing import Annotated
from uuid import UUID, uuid4

from fastapi import APIRouter, Depends, HTTPException, Request, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from sthali_db import ModelType, SchemaType
from ..dependencies import paginate_parameters
from . import Base


class API(Base):
    """{...}."""

    prefix = "/api/v1"

    def __init__(self, *args, **kwargs) -> None:
        """{...}."""
        super().__init__(*args, **kwargs)

    @property
    def local_context(self) -> dict[str, str]:
        """Base context for current view templates.

        Returns:
        -------
            Dictionary with base context values.

        """
        return {
            "url_for_api_create": f"api_create_{self.resource_name}",
            "url_for_api_read": f"api_read_{self.resource_name}",
            "url_for_api_update": f"api_update_{self.resource_name}",
            "url_for_api_delete": f"api_delete_{self.resource_name}",
            "url_for_api_read_many": f"api_read_many_{self.resource_name}",
        }

    def _make_create_endpoint(self):
        """Factory for create endpoint with injected dependencies."""
        model = self.model
        handle_result = self.handle_result
        CreateSchema = self.create_schema

        async def create_endpoint(
            db: Annotated[AsyncSession, Depends(self.get_db)],
            resource: CreateSchema,
        ) -> SchemaType:
            resource_id = uuid4()
            resource_obj = resource.model_dump()
            obj = model(**resource_obj, id=resource_id)
            db.add(obj)
            await db.commit()
            return handle_result(obj)

        return create_endpoint

    def _make_read_endpoint(self):
        """Factory for read endpoint with injected dependencies."""
        model = self.model
        handle_result = self.handle_result

        async def read_endpoint(
            db: Annotated[AsyncSession, Depends(self.get_db)],
            resource_id: UUID,
        ) -> SchemaType:
            result = await db.get(model, resource_id)
            return handle_result(result)

        return read_endpoint

    def _make_update_endpoint(self):
        """Factory for update endpoint with injected dependencies."""
        model = self.model
        handle_result = self.handle_result
        UpdateSchema = self.update_schema

        async def update_endpoint(
            db: Annotated[AsyncSession, Depends(self.get_db)],
            request: Request,
            resource_id: UUID,
            resource: UpdateSchema,
        ) -> SchemaType:
            result = await db.get(model, resource_id)
            if not result:
                raise HTTPException(status.HTTP_404_NOT_FOUND, "Resource not found")

            partial = request.method == "PATCH"
            resource_obj = resource.model_dump(exclude_unset=partial)

            for key, value in resource_obj.items():
                setattr(result, key, value)
            await db.commit()
            await db.refresh(result)
            return handle_result(result)

        return update_endpoint

    def _make_delete_endpoint(self):
        """Factory for delete endpoint with injected dependencies."""
        model = self.model

        async def delete_endpoint(
            db: Annotated[AsyncSession, Depends(self.get_db)],
            resource_id: UUID,
        ) -> None:
            result = await db.get(model, resource_id)
            if result:
                await db.delete(result)
                await db.commit()

        return delete_endpoint

    def _make_read_many_endpoint(self):
        """Factory for read_many endpoint with injected dependencies."""
        model = self.model
        handle_list_result = self.handle_list_result

        async def read_many_endpoint(
            db: Annotated[AsyncSession, Depends(self.get_db)],
            paginate_params: paginate_parameters = None,
        ) -> list[SchemaType]:
            query = await db.execute(select(model))
            result: list[ModelType] = query.scalars().all()  # type: ignore
            return handle_list_result(result)

        return read_many_endpoint

    @property
    def api_router(self) -> APIRouter:
        router = APIRouter(prefix=f"/{self.resource_name}", tags=["api", self.resource_name])
        router.add_api_route(
            "/",
            self._make_create_endpoint(),
            name=f"api_create_{self.resource_name}",
            response_model=self.read_schema,
            methods=["POST"],
            status_code=201,
        )
        router.add_api_route(
            "/{resource_id}/",
            self._make_read_endpoint(),
            name=f"api_read_{self.resource_name}",
            response_model=self.read_schema,
            methods=["GET"],
        )
        router.add_api_route(
            "/{resource_id}/",
            self._make_update_endpoint(),
            name=f"api_update_{self.resource_name}",
            response_model=self.read_schema,
            methods=["PUT"],
        )
        router.add_api_route(
            "/{resource_id}/",
            self._make_update_endpoint(),
            name=f"api_update_{self.resource_name}",
            response_model=self.read_schema,
            methods=["PATCH"],
        )
        router.add_api_route(
            "/{resource_id}/",
            self._make_delete_endpoint(),
            name=f"api_delete_{self.resource_name}",
            response_model=None,
            methods=["DELETE"],
            status_code=204,
        )
        router.add_api_route(
            "/",
            self._make_read_many_endpoint(),
            name=f"api_read_many_{self.resource_name}",
            response_model=list[self.read_schema],
            methods=["GET"],
        )
        return router

