import typing
import uuid

import pydantic
import sthali_db

class Base(pydantic.BaseModel):
    pass


class BaseWithId(Base):
    id: typing.Annotated[uuid.UUID, pydantic.Field(description="Resource identifier")]


class Models:
    name: str
    create_model: type[Base]
    response_model: type[Base]
    update_model: type[Base]

    def __init__(self, name: str, fields: list[sthali_db.Field]) -> None:
        self.name = name
        self.create_model = self.define_model(Base, f"Create{name.title()}", fields)
        self.response_model = self.define_model(BaseWithId, f"Response{name.title()}", fields)
        self.update_model = self.define_model(Base, f"Update{name.title()}", fields)

    @staticmethod
    def define_model(base: type[Base], name: str, fields: list[sthali_db.Field]) -> type[Base]:
        fields_constructor = {}
        for field in fields:
            field_type = (field.type, field.type | None)[bool(field.allow_none)]
            pydantic_field = pydantic.Field(description=field.description or f"Field {field.name}")
            if field.has_default or field.default_value:
                pydantic_field.default = field.default_value

            fields_constructor[field.name] = typing.Annotated[field_type, pydantic_field]

        return pydantic.create_model(__model_name=name, __base__=base, **fields_constructor)  # type: ignore
