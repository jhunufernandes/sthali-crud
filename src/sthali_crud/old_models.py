from uuid import UUID, uuid4
from types import UnionType
from typing import Any, Literal, LiteralString
from pydantic import BaseModel, create_model, Field
from .types import FieldDefinition, ModelStrategy, ResourceSpecification


class CreateInputModel(BaseModel):
    pass


class UpdateInputModel(BaseModel):
    id: UUID = Field(default_factory=uuid4)


class UpsertInputModel(BaseModel):
    pass


class ResponseModel(BaseModel):
    id: UUID = Field(default_factory=uuid4)


class Models:
    _create_input_model = CreateInputModel
    _update_input_model = UpdateInputModel
    _upsert_input_model = UpsertInputModel
    _response_model = ResponseModel

    @property
    def create_input_model(self):
        return self._create_input_model

    @property
    def update_input_model(self):
        return self._update_input_model

    @property
    def upsert_input_model(self):
        return self._upsert_input_model

    @property
    def response_model(self):
        return self._response_model

    # @classmethod
    # def replace_model(cls, model: type[BaseModel]) -> None:
    #     cls._model = model

    # def _get_model(self, strategy: Literal['CREATE', 'UPSERT', 'UPDATE']) -> BaseModel:
    #     _model_attr: str = f'_{strategy.lower()}_resource_model'
    #     return getattr(self, _model_attr)

    def __init__(self, resource_spec: ResourceSpecification) -> None:
        _model_strategy = self.resolve_spec(resource_spec)
        self._create_input_model = _model_strategy.create_input_model
        self._upsert_input_model = _model_strategy.upsert_input_model
        self._update_input_model = _model_strategy.update_input_model
        self._response_model = _model_strategy.response_model

    @staticmethod
    def define_model(
            base: type[BaseModel],
            name: str,
            fields: list[FieldDefinition]):
        _fields_constructor: dict = {}
        for _field in fields:
            _field_name: str = _field.name
            # _field_default_value: Any = (..., _field.default_value)[_field.default_value or _field.has_default or strategy in ('CREATE', 'UPSERT')]
            _field_default_value: Any = (..., _field.default_value)[_field.has_default]
            _field_type: type | UnionType = (_field.type, _field.type | None)[_field.allow_none]
            _fields_constructor[_field_name] = (_field_type, _field_default_value)

        return create_model(__model_name=name, __base__=base, **_fields_constructor)

    @staticmethod
    def resolve_spec(resource_spec: ResourceSpecification) -> ModelStrategy:
        _create_input_model = Models.define_model(
            base=CreateInputModel,
            name=f'Create{resource_spec.name.title()}',
            fields=resource_spec.fields)
        _update_input_model = Models.define_model(
            base=UpdateInputModel,
            name=f'Update{resource_spec.name.title()}',
            fields=resource_spec.fields)
        _upsert_input_model = Models.define_model(
            base=UpsertInputModel,
            name=f'Upsert{resource_spec.name.title()}',
            fields=resource_spec.fields)
        return ModelStrategy(
            create_input_model=_create_input_model,
            upsert_input_model=_upsert_input_model,
            update_input_model=_update_input_model,
            response_model=_update_input_model,
        )

        # _models_constructor: dict[Strategy, BaseModel] = {}

        # for _strategy, _strategy_model in STRATEGY_INPUT_MODEL.items():
        #     _model_name: str = ''.join([k.title() for k in [_strategy, resource_spec.name]])
        #     _model_definition: BaseModel = Models.define_model(
        #         base=_strategy_model,
        #         name=_model_name,
        #         fields=resource_spec.fields,
        #         strategy=_strategy)
        #     _models_constructor[_strategy] = _model_definition
        # return ModelStrategy(**_models_constructor)
