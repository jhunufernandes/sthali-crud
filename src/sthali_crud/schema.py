"""Methods for Schema.
"""
from typing import Optional
from pydantic import BaseModel, create_model
from .types import Field


class Schema:
    """Schema main class.
    """
    def __init__(self, name: str, fields: list[Field]) -> None:
        self._name = name
        self._fields = fields

    @property
    def model(self) -> type[BaseModel]:
        """model property.

        Returns:
            type[BaseModel]: Pydantic model.
        """
        return create_model(self._name,
                            **{field.name: ((field.type, Optional[field.type])[field.allow_none], field.default or ...)
                               for field in self._fields})  # type: ignore
