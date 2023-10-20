"""Methods for Schema.
"""
from typing import Any, Literal, Type
from uuid import UUID, uuid4
from pydantic import BaseModel, create_model as define_model, Field
from pydantic.dataclasses import dataclass


@dataclass
class FieldDefinition:
    """Field definition.
    """
    name: str
    type: type
    has_default: bool = False
    default_value: Any = None
    allow_none: bool = False


class Base(BaseModel):
    """Base main class.
    """
    id: UUID = Field(default_factory=uuid4)


class Schema:
    """Schema main class.
    """
    _create_model: Type[Base]
    _update_model: Type[Base]
    _upsert_model: Type[Base]

    def __init__(self, name: str, fields: list[FieldDefinition]) -> None:
        for strategy in ['CREATE', 'UPDATE', 'UPSERT']:
            model_name: str = f'_{strategy.lower}_{name.lower()}'
            model_definition: Type[Base] = self._define_model(base=Base, name=f'{strategy}{name.title()}',
                                                              fields=fields, strategy=strategy)  # type: ignore
            self.__setattr__(model_name, model_definition)

    @property
    def create_model(self) -> type[Base]:
        return self._create_model

    @property
    def put_model(self) -> type[Base]:
        return self._put_model

    @property
    def patch_model(self) -> type[Base]:
        return self._patch_model

    @staticmethod
    def _define_model(base: Type[Base], name: str, fields: list[FieldDefinition],
                      strategy: Literal['CREATE', 'UPDATE', 'UPSERT']) -> Type[Base]:
        fields_constructor = {}
        for field in fields:
            _field_name = field.name
            _field_default_value = (..., field.default_value)[field.has_default or strategy in ('CREATE', 'UPSERT')]
            _field_type = (field.type, field.type | None)[field.allow_none]
            fields_constructor[_field_name] = (_field_type, _field_default_value)

        return create_model(name, __base__=base, **fields_constructor)
