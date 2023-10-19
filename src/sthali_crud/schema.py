"""Methods for Schema.
"""
from uuid import UUID, uuid4
from pydantic import BaseModel, ConfigDict, create_model, Field as PydanticField
from .types import Field, Model


class Base(BaseModel):
    """Base main class.
    """
    id: UUID = PydanticField(default_factory=uuid4)

    model_config = ConfigDict(extra='allow')


class Schema:
    """Schema main class.
    """
    _model: Base

    def __init__(self, name: str, fields: list[Field]) -> None:
        self._model = self._create_model(base=Base, name=name, fields=fields)

    @property
    def model(self) -> Model:
        """model property.

        Returns:
            Model: Pydantic model.
        """
        return self._model

    @staticmethod
    def _create_model(base: Model, name: str, fields: list[Field]) -> Model:
        fields_constructor = {}
        for field in fields:
            default = field.default or ...
            none = (field.type, field.type | None)[field.allow_none]
            fields_constructor[field.name] = (none, default)

        return create_model(name, __base__=base, **fields_constructor)
