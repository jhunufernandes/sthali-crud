"""{...}."""

from uuid import UUID

from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from sqlalchemy import select

from ..database import DbSession, ModelType
from ..templates import templates
from . import Base


class VIEWS(Base):
    """{...}."""

    def __init__(self, *args, create_template: str, read_template: str, read_many_template: str, **kwargs) -> None:
        """{...}."""
        super().__init__(*args, **kwargs)

        self.create_template = create_template
        self.read_template = read_template
        self.read_many_template = read_many_template

    async def view_create(self, request: Request) -> HTMLResponse:
        """{...}."""
        context = {
            "form_fields": self.schema.get_form_fields(),
            "submit_url": f"/api/v1/{self.resource_name}",
            "callback": self.resource_name,
        }
        return templates.TemplateResponse(request, "crud/create.html", context)

    async def view_read(
        self,
        request: Request,
        db: DbSession,
        resource_id: UUID,
    ) -> HTMLResponse:
        """{...}."""
        result = await db.get(self.model, resource_id)

        ignore_fields = ["id"]
        disable_fields = ["id"]
        context = {
            "form_fields": self.schema.get_form_fields(ignore_fields, disable_fields),
            "submit_url": f"/api/v1/{self.resource_name}",
            "resource": self._handle_result(result).model_dump(),
            "callback": self.resource_name,
        }
        return templates.TemplateResponse(request, "crud/read.html", context)

    async def view_read_many(self, request: Request, db: DbSession) -> HTMLResponse:
        """{...}."""
        query = await db.execute(select(self.model))
        result: list[ModelType] = query.scalars().all()  # type: ignore[]
        context = {
            "resources": self._handle_list_result(result) * 100,
            "model_fields": self.schema.model_fields,
        }
        return templates.TemplateResponse(request, "crud/read_many.html", context)

    @property
    def api_router(self) -> APIRouter:
        """{...}."""
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
