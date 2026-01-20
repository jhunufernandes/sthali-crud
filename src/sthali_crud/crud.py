"""SthaliCRUD class for dynamic router generation."""
from fastapi import APIRouter

from .database.models import BaseModel
from .database.schemas import BaseSchema
from .routers.api import API
from .routers.views import VIEWS


class CRUD:
    """A class that dynamically creates and manages API and Views routers."""

    def __init__(
        self,
        model: type[BaseModel],
        create_schema: type[BaseSchema],
        read_schema: type[BaseSchema],
        update_schema: type[BaseSchema],
        create_template: str,
        read_template: str,
        read_many_template: str,
    ) -> None:
        """Initialize SthaliCRUD with model and schemas.

        Args:
            model: The SQLAlchemy database model class.
            create_schema: The create request schema class.
            read_schema: The response schema class.
            update_schema: The update request schema class.
            create_template: Path to create form template.
            read_template: Path to read/edit form template.
            read_many_template: Path to list view template.

        """
        self.api = API(model, read_schema, create_schema, update_schema)
        self.views = VIEWS(
            # model,
            read_schema,
            create_schema,
            update_schema,
            create_template=create_template,
            read_template=read_template,
            read_many_template=read_many_template,
        )
