from uuid import UUID

from pydantic import BaseModel, create_model

from src.sthali_crud.types import FieldDefinition


class Base(BaseModel):
    pass


class BaseWithId(Base):
    id: UUID


class BaseWithIdOptional(Base):
    id: UUID | None = None


class BaseWithStrId(Base):
    id: str


class Models:
    name: str

    create_model: type[BaseModel]
    response_model: type[BaseModel]
    update_model: type[BaseModel]

    def __init__(self, name: str, fields: list[FieldDefinition]) -> None:
        self.name = name
        self.create_model = self.define_model(Base, f"Create{name.title()}", fields)
        self.response_model = self.define_model(
            BaseWithStrId, f"Response{name.title()}", fields
        )
        self.update_model = self.define_model(
            BaseWithId, f"Update{name.title()}", fields
        )
        self.upsert_model = self.define_model(
            BaseWithIdOptional, f"Upsert{name.title()}", fields
        )

    @staticmethod
    def define_model(
        base: type[BaseModel], name: str, fields: list[FieldDefinition]
    ) -> type[BaseModel]:
        _fields_constructor = {}
        for _field in fields:
            _field_name = _field.name
            _field_default_value = (..., _field.default_value)[_field.has_default]
            _field_type = (_field.type, _field.type | None)[_field.allow_none]
            _fields_constructor[_field_name] = (_field_type, _field_default_value)

        return create_model(__model_name=name, __base__=base, **_fields_constructor)
