from typing import Any, List

from pydantic import BaseModel, create_model

from .types import Field


class Schema(BaseModel):
    """Schema
    """
    name: str
    fields: List[Field]

    @property
    def response_model(self) -> Any:
        """response_model
        """
        return create_model(
            self.name,
            **{field.name: (field.type, (None, ...)[field.required])
               for field in self.fields}  # type: ignore
        )
