"""RESTful CRUD API router for Sthali models."""

from collections.abc import Callable
from typing import Annotated, Any, ClassVar
from uuid import UUID, uuid4

from fastapi import APIRouter, Depends, HTTPException, Request, status
from sqlalchemy import select
from sthali_db import DBSession, ModelType, SchemaType
from sthali_db.engine import session_ctx

from ..dependencies import paginate_parameters
from . import Base


def replace_type_hint(
    original_func: Callable[..., Any],
    type_name: str,
    new_type: SchemaType,
) -> Callable[..., Any]:
    """Mutate the annotation of a named parameter on a function in place.

    Args:
        original_func: The function whose annotation will be replaced.
        type_name: The parameter name whose annotation should be replaced.
        new_type: The new type to assign to that parameter.

    Returns:
        The same function with the updated annotation.
    """
    if original_func.__annotations__ and type_name in original_func.__annotations__:
        original_func.__annotations__[type_name] = new_type
    return original_func


class API(Base):
    """CRUD API router exposing standard REST endpoints for a Sthali model."""

    prefix: ClassVar[str] = "/api/v1"

    def __init__(self, *args, **kwargs) -> None:
        """Forward all arguments to the base router initialiser."""
        super().__init__(*args, **kwargs)

    @property
    def local_context(self) -> dict[str, str]:
        """URL route names for this resource's API endpoints.

        Returns:
            Mapping of context keys to FastAPI route names.
        """
        return {
            "url_for_api_create": f"api_create_{self.resource_name}",
            "url_for_api_read": f"api_read_{self.resource_name}",
            "url_for_api_update": f"api_update_{self.resource_name}",
            "url_for_api_delete": f"api_delete_{self.resource_name}",
            "url_for_api_read_many": f"api_read_many_{self.resource_name}",
        }

    @property
    def create_endpoint(self) -> Callable[..., Any]:
        """Return the async create endpoint function."""
        return self._make_create_endpoint()

    @property
    def read_endpoint(self) -> Callable[..., Any]:
        """Return the async read endpoint function."""
        return self._make_read_endpoint()

    @property
    def update_endpoint(self) -> Callable[..., Any]:
        """Return the async update endpoint function."""
        return self._make_update_endpoint()

    @property
    def delete_endpoint(self) -> Callable[..., Any]:
        """Return the async delete endpoint function."""
        return self._make_delete_endpoint()

    @property
    def read_many_endpoint(self) -> Callable[..., Any]:
        """Return the async read-many endpoint function."""
        return self._make_read_many_endpoint()

    @property
    def api_router(self) -> APIRouter:
        """Build and return the FastAPI APIRouter with all CRUD routes registered."""
        router = APIRouter(prefix=f"/{self.resource_name}", tags=["api", self.resource_name])
        router.add_api_route(
            "/",
            replace_type_hint(self.create_endpoint, "resource", self.create_schema),
            name=f"api_create_{self.resource_name}",
            response_model=self.read_schema,
            methods=["POST"],
            status_code=201,
        )
        router.add_api_route(
            "/{resource_id}/",
            self.read_endpoint,
            name=f"api_read_{self.resource_name}",
            response_model=self.read_schema,
            methods=["GET"],
        )
        router.add_api_route(
            "/{resource_id}/",
            replace_type_hint(self.update_endpoint, "resource", self.update_schema),
            name=f"api_update_{self.resource_name}",
            response_model=self.read_schema,
            methods=["PUT"],
        )
        router.add_api_route(
            "/{resource_id}/",
            replace_type_hint(self.update_endpoint, "resource", self.update_schema),
            name=f"api_update_{self.resource_name}",
            response_model=self.read_schema,
            methods=["PATCH"],
        )
        router.add_api_route(
            "/{resource_id}/",
            self.delete_endpoint,
            name=f"api_delete_{self.resource_name}",
            response_model=None,
            methods=["DELETE"],
            status_code=204,
        )
        router.add_api_route(
            "/",
            self.read_many_endpoint,
            name=f"api_read_many_{self.resource_name}",
            response_model=list[self.read_schema],
            methods=["GET"],
        )
        return router

    def _make_create_endpoint(self) -> Callable[..., Any]:
        async def create_endpoint(
            db_session: Annotated[DBSession, Depends(self.db_session)],
            resource: SchemaType,
        ) -> SchemaType:
            async with session_ctx(self.db_session, db_session) as session:
                resource_id = uuid4()
                resource_obj = resource.model_dump()
                resource = self.model(**resource_obj, id=resource_id)
                session.add(resource)
                await session.commit()
                return self.handle_result(resource)

        return create_endpoint

    def _make_read_endpoint(self) -> Callable[..., Any]:
        async def read_endpoint(
            db_session: Annotated[DBSession, Depends(self.db_session)],
            resource_id: UUID,
        ) -> SchemaType:
            async with session_ctx(self.db_session, db_session) as session:
                result = await session.get(self.model, resource_id)
                return self.handle_result(result)

        return read_endpoint

    def _make_update_endpoint(self) -> Callable[..., Any]:
        async def update_endpoint(
            db_session: Annotated[DBSession, Depends(self.db_session)],
            request: Request,
            resource_id: UUID,
            resource: SchemaType,
        ) -> SchemaType:
            async with session_ctx(self.db_session, db_session) as session:
                result = await session.get(self.model, resource_id)
                if not result:
                    raise HTTPException(status.HTTP_404_NOT_FOUND, "Resource not found")

                partial = request.method == "PATCH"
                resource_obj = resource.model_dump(exclude_unset=partial)

                for key, value in resource_obj.items():
                    setattr(result, key, value)
                await session.commit()
                await session.refresh(result)
                return self.handle_result(result)

        return update_endpoint

    def _make_delete_endpoint(self) -> Callable[..., Any]:
        async def delete_endpoint(
            db_session: Annotated[DBSession, Depends(self.db_session)],
            resource_id: UUID,
        ) -> None:
            async with session_ctx(self.db_session, db_session) as session:
                await session.delete(resource_id)
                await session.commit()

        return delete_endpoint

    def _make_read_many_endpoint(self) -> Callable[..., Any]:
        async def read_many_endpoint(
            db_session: Annotated[DBSession, Depends(self.db_session)],
            _paginate_parameters: paginate_parameters = None,
        ) -> list[SchemaType]:
            async with session_ctx(self.db_session, db_session) as session:
                query = await session.execute(select(self.model))
                result: list[ModelType] = query.scalars().all()  # type: ignore[assignment]
                return self.handle_list_result(result)

        return read_many_endpoint
