from uuid import UUID

from pydantic import BaseModel, create_model

from .types import FieldDefinition


class Base(BaseModel):
    pass


class BaseWithId(Base):
    id: UUID


class BaseWithIdOptional(Base):
    id: UUID | None = None


class Models:
    name: str
    create_model: type[Base]
    response_model: type[Base]
    update_model: type[Base]
    upsert_model: type[Base]

    def __init__(self, name: str, fields: list[FieldDefinition]) -> None:
        self.name = name
        self.create_model = self.define_model(Base, f"Create{name.title()}", fields)
        self.response_model = self.define_model(
            BaseWithId, f"Response{name.title()}", fields
        )
        self.update_model = self.define_model(
            BaseWithId, f"Update{name.title()}", fields
        )
        self.upsert_model = self.define_model(
            BaseWithIdOptional, f"Upsert{name.title()}", fields
        )

    @staticmethod
    def define_model(
        base: type[Base], name: str, fields: list[FieldDefinition]
    ) -> type[Base]:
        fields_constructor = {}
        for field in fields:
            field_default_value = (..., field.default_value)[
                bool(field.default_value or field.has_default)
            ]
            fields_constructor[field.name] = (field.type, field_default_value)

        return create_model(__model_name=name, __base__=base, **fields_constructor)  # type: ignore
