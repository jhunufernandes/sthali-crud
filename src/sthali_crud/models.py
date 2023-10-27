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
        fields_constructor = {}
        for field in fields:
            field_default_value = (..., field.default_value)[field.default_value or field.has_default]
            field_type = (field.type, field.type | None)[field.allow_none]
            fields_constructor[field.name] = (field_type, field_default_value)

        return create_model(__model_name=name, __base__=base, **fields_constructor)
