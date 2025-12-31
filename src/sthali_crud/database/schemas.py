"""{...}."""

from typing import Any, AnyStr, TypeVar
from uuid import UUID

from pydantic import BaseModel


def get_field_form_type(_type: type) -> str:
    """{...}."""
    if _type == UUID:
        return "text"
    if _type == AnyStr:
        return "text"
    return "text"


class BaseSchema(BaseModel):
    """{...}."""

    class Config:
        """{...}."""

        from_attributes = True

    @classmethod
    def get_form_fields(
        cls,
        ignore_fields: list[str] | None = None,
        disabled_fields: list[str] | None = None,
    ) -> dict[str, dict[str, str]]:
        """{...}."""
        ignore_fields = ignore_fields or []
        disabled_fields = disabled_fields or []
        _model_fields = {}
        for k, v in cls.model_fields.items():
            if k in ignore_fields:
                continue
            _model_fields[k] = {
                "type": get_field_form_type(v.annotation),
                "disabled": "disabled" if k in disabled_fields else "",
            }
        return _model_fields

    def model_dump(self, **kwargs) -> dict[str, Any]:
        """Overrides the default model_dump to add extra data."""
        data = super().model_dump(**kwargs)
        if not hasattr(self, "id"):
            return data
        return {
            **data,
            "_links": {"self": f"/api/v1/{self.__class__.__name__.lower().replace('schema', '')}s/{self.id}"},
        }


SchemaType = TypeVar("SchemaType", bound=BaseSchema)


class RoleCreateSchema(BaseSchema):
    """{...}."""

    name: str


class RoleSchema(RoleCreateSchema):
    """{...}."""

    id: UUID
