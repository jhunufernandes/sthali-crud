"""Methods for Schema.
"""
from typing import Any, Literal, Type
from uuid import UUID, uuid4
from pydantic import BaseModel, create_model, Field
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


@dataclass
class ResourceSpec:
    """Resource specification.
    """
    name: str
    fields: list[FieldDefinition]


class Base(BaseModel):
    """Base main class.
    """


class BaseWithId(Base):
    """Base main class with id.
    """
    id: UUID = Field(default_factory=uuid4)


STRATEGY_BASE_MODEL = {
    'CREATE': Base,
    'READ': BaseWithId,
    'UPDATE': BaseWithId,
    'UPSERT': Base,
}


class Schema:
    """Schema main class.
    """
    _create_resource: Type[Base]
    _read_resource: Type[Base]
    _update_resource: Type[Base]
    _upsert_resource: Type[Base]

    def __init__(self, name: str, fields: list[FieldDefinition]) -> None:
        for strategy, strategy_model in STRATEGY_BASE_MODEL.items():
            _model_name: str = f'_{strategy.lower}_{name.lower()}'
            _model_definition: Type[Base] = self.create_model(base=strategy_model, name=f'{strategy}{name.title()}',
                                                              fields=fields, strategy=strategy)  # type: ignore
            self.__setattr__(_model_name, _model_definition)

    @property
    def create_resource(self) -> type[Base]:
        return self._create_resource

    @property
    def read_resource(self) -> type[Base]:
        return self._read_resource

    @property
    def update_resource(self) -> type[Base]:
        return self._update_resource

    @property
    def upsert_resource(self) -> type[Base]:
        return self._upsert_resource

    @staticmethod
    def create_model(base: Type[Base], name: str, fields: list[FieldDefinition],
                     strategy: Literal['CREATE', 'READ', 'UPDATE', 'UPSERT']) -> Type[Base]:
        _fields_constructor: dict = {}
        for _field in fields:
            _field_name: str = _field.name
            # _field_default_value: Any = (..., _field.default_value)[_field.default_value or _field.has_default or strategy in ('CREATE', 'UPSERT')]
            _field_default_value: Any = (..., _field.default_value)[_field.has_default]
            _field_type: type = (_field.type, _field.type | None)[_field.allow_none]
            _fields_constructor[_field_name] = (_field_type, _field_default_value)

        return create_model(name, __base__=base, **_fields_constructor)
