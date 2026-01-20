"""Pydantic schemas for API request/response models.

This module provides base schemas with form field generation and HATEOAS support.
"""

from typing import Any, TypeVar, get_args, get_origin
from uuid import UUID

from pydantic import BaseModel


def get_field_form_type(_type: type) -> str:
    """Map Python types to HTML form input types.

    Args:
    ----
        _type: The Python type to map.

    Returns:
    -------
        The corresponding HTML input type.

    """
    origin = get_origin(_type)
    if origin is not None:
        args = get_args(_type)
        # Filter out NoneType from Optional/Union types
        args = [arg for arg in args if arg is not type(None)]
        if args:
            _type = args[0]

    type_mapping = {
        UUID: "text",
        str: "text",
        int: "number",
        float: "number",
        bool: "checkbox",
    }
    return type_mapping.get(_type, "text")


class BaseSchema(BaseModel):
    """Base schema with form field generation and HATEOAS link support."""

    class Config:
        """Pydantic model configuration."""

        from_attributes = True

    @classmethod
    def get_form_fields(
        cls,
        ignore_fields: list[str] | None = None,
        disabled_fields: list[str] | None = None,
    ) -> dict[str, dict[str, str]]:
        """Generate form field metadata for frontend rendering.

        Args:
        ----
            ignore_fields: Fields to exclude from the form.
            disabled_fields: Fields that should be disabled in the form.

        Returns:
        -------
            Dictionary mapping field names to their form metadata.

        """
        ignore_fields = ignore_fields or []
        disabled_fields = disabled_fields or []
        _model_fields = {}
        for k, v in cls.model_fields.items():
            if k in ignore_fields:
                continue
            _model_fields[k] = {
                "type": get_field_form_type(v.annotation),
                "disabled": "disabled" if k in disabled_fields else "",
                "required": "required" if v.is_required() else "",
            }
        return _model_fields

    def model_dump(self, **kwargs) -> dict[str, Any]:
        """Override model_dump to add HATEOAS links.

        Args:
        ----
            **kwargs: Arguments to pass to the parent model_dump.

        Returns:
        -------
            Model data with HATEOAS links if applicable.

        """
        data = super().model_dump(**kwargs)
        if not hasattr(self, "id"):
            return data

        resource_name = self.__class__.__name__.lower().replace("schema", "").replace("read", "")
        return {
            **data,
            "_links": {"self": f"/api/v1/{resource_name}s/{self.id}"},
        }


SchemaType = TypeVar("SchemaType", bound=BaseSchema)


class RoleCreateSchema(BaseSchema):
    """Schema for creating a new role."""

    name: str


RoleUpdateSchema = RoleCreateSchema


class RoleReadSchema(RoleCreateSchema):
    """Schema for reading role data with ID."""

    id: UUID
