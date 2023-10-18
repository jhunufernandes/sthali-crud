"""Methods for Schema.
"""
from pydantic import BaseModel, create_model
from .types import Field, Model


class Schema:
    """Schema main class.
    """
    _model: Model
    _model_without_id: Model

    class Base(BaseModel):
        """Base main class.
        """
        id: int

    def __init__(self, name: str, fields: list[Field]) -> None:
        self._model = self._create_model(base=self.Base, name=name, fields=fields)
        self._model_without_id = self._create_model(base=BaseModel, name=f'{name}_without_id', fields=fields)

    @property
    def model(self) -> Model:
        """model property.

        Returns:
            Model: Pydantic model.
        """
        return self._model

    @property
    def model_without_id(self) -> Model:
        """model property without field id.

        Returns:
            Model: Pydantic model.
        """
        return self._model_without_id

    @staticmethod
    def _create_model(base: Model, name: str, fields: list[Field]) -> Model:
        fields_constructor = {}
        for field in fields:
            default = field.default or ...
            none = (field.type, field.type | None)[field.allow_none]
            fields_constructor[field.name] = (none, default)

        return create_model(name, __base__=base, **fields_constructor)
