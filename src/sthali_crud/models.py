from pydantic import BaseModel, create_model

from .types import (
    CreateModel,
    FieldDefinition,
    ModelStrategy,
    ResourceSpecification,
    ResponseModel,
    UpdateModel,
    UpsertModel,
)


class Models:
    """Models main class."""

    resource: str
    create_model: type[CreateModel]
    response_model: type[ResponseModel]
    update_model: type[UpdateModel]
    upsert_model: type[UpsertModel]

    def __init__(self, resource_spec: ResourceSpecification) -> None:
        self._resource = resource_spec.name
        _model_strategy = self.resolve_spec(resource_spec)
        self.create_model = _model_strategy.create_model
        self.response_model = _model_strategy.response_model
        self.update_model = _model_strategy.update_model
        self.upsert_model = _model_strategy.upsert_model

    @staticmethod
    def define_model(base: type[BaseModel], name: str, fields: list[FieldDefinition]):
        """Get field definition and apply on create_model().

        Args:
            base (type[BaseModel]): BaseModel for create_model().
            name (str): Model name.
            fields (list[FieldDefinition]): List of field definition.

        Returns:
            _type_: Model created.
        """
        _fields_constructor = {}
        for _field in fields:
            _field_name = _field.name
            _field_default_value = (..., _field.default_value)[_field.has_default]
            _field_type = (_field.type, _field.type | None)[_field.allow_none]
            _fields_constructor[_field_name] = (_field_type, _field_default_value)

        return create_model(__model_name=name, __base__=base, **_fields_constructor)

    @staticmethod
    def resolve_spec(resource_spec: ResourceSpecification) -> ModelStrategy:
        """Resolve resource specification and apply on define_model().

        Args:
            resource_spec (ResourceSpecification): Resource specification.

        Returns:
            ModelStrategy: Models defined by route strategy.
        """
        _create_input_model = Models.define_model(
            base=CreateModel,
            name=f"Create{resource_spec.name.title()}",
            fields=resource_spec.fields,
        )
        _response_model = Models.define_model(
            base=ResponseModel,
            name=f"Response{resource_spec.name.title()}",
            fields=resource_spec.fields,
        )
        _update_input_model = Models.define_model(
            base=UpdateModel,
            name=f"Update{resource_spec.name.title()}",
            fields=resource_spec.fields,
        )
        _upsert_input_model = Models.define_model(
            base=UpsertModel, name=f"Upsert{resource_spec.name.title()}", fields=[]
        )
        return ModelStrategy(
            create_model=_create_input_model,
            response_model=_response_model,
            update_model=_update_input_model,
            upsert_model=_upsert_input_model,
        )
