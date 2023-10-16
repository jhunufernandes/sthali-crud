"""Methods for Schema.
"""
from typing import Optional
from pydantic import create_model
from .types import Field, Model


class Schema:
    """Schema main class.
    """
    def __init__(self, name: str, fields: list[Field]) -> None:
        self._name = name
        self._fields = fields

    @property
    def model(self) -> Model:
        """model property.

        Returns:
            Model: Pydantic model.
        """
        return create_model(self._name,
                            **{field.name: ((field.type, Optional[field.type])[field.allow_none], field.default or ...)
                               for field in self._fields})  # type: ignore
