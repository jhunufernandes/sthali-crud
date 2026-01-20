"""View handlers for rendering HTML templates for CRUD operations."""

from uuid import UUID

from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from sqlalchemy import select

from ..database import DbSession, ModelType
from ..templates import templates
from . import Base


class VIEWS(Base):
    """HTML view handler for CRUD operations with customizable templates."""

    def __init__(
        self,
        *args,
        create_template: str,
        read_template: str,
        read_many_template: str,
        **kwargs,
    ) -> None:
        """Initialize the VIEWS handler.

        Args:
        ----
            *args: Positional arguments passed to parent Base class.
            create_template: Path to the create form template.
            read_template: Path to the read/edit form template.
            read_many_template: Path to the list view template.
            **kwargs: Keyword arguments passed to parent Base class.

        """
        super().__init__(*args, **kwargs)

        self.create_template = create_template
        self.read_template = read_template
        self.read_many_template = read_many_template

    async def view_create(self, request: Request) -> HTMLResponse:
        """Render the create form view.

        Args:
        ----
            request: The HTTP request object.

        Returns:
        -------
            HTML response with create form template.

        """
        context = {
            "form_fields": self.read_schema.get_form_fields(),
            "submit_url": f"/api/v1/{self.resource_name}",
            "callback": self.resource_name,
        }
        return templates.TemplateResponse(request, self.create_template, context)

    async def view_read(
        self,
        request: Request,
        db: DbSession,
        resource_id: UUID,
    ) -> HTMLResponse:
        """Render the read/edit view for a single resource.

        Args:
        ----
            request: The HTTP request object.
            db: Database session dependency.
            resource_id: The ID of the resource to read.

        Returns:
        -------
            HTML response with read form template.

        """
        result = await db.get(self.model, resource_id)

        ignore_fields = ["id"]
        disable_fields = ["id"]
        context = {
            "form_fields": self.read_schema.get_form_fields(ignore_fields, disable_fields),
            "submit_url": f"/api/v1/{self.resource_name}",
            "resource": self._handle_result(result).model_dump(),
            "callback": self.resource_name,
        }
        return templates.TemplateResponse(request, self.read_template, context)

    async def view_read_many(self, request: Request, db: DbSession) -> HTMLResponse:
        """Render the list view for multiple resources.

        Args:
        ----
            request: The HTTP request object.
            db: Database session dependency.

        Returns:
        -------
            HTML response with list template showing all resources.

        """
        query = await db.execute(select(self.model))
        result: list[ModelType] = query.scalars().all()  # type: ignore[]
        context = {
            "resources": self._handle_list_result(result),
            "model_fields": self.read_schema.model_fields,
        }
        return templates.TemplateResponse(request, self.read_many_template, context)

    @property
    def api_router(self) -> APIRouter:
        """Create and configure the API router for view endpoints.

        Returns:
        -------
            Configured APIRouter with view routes.

        """
        router = APIRouter(prefix=f"/{self.resource_name}", tags=[self.resource_name])
        router.add_api_route(
            "/",
            self.view_read_many,
            response_class=HTMLResponse,
            methods=["GET"],
        )
        router.add_api_route(
            "/new",
            self.view_create,
            response_class=HTMLResponse,
            methods=["GET"],
        )
        router.add_api_route(
            "/{resource_id}",
            self.view_read,
            response_class=HTMLResponse,
            methods=["GET"],
        )
        return router
