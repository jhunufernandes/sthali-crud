from types import UnionType
from typing import Any, Literal
from pydantic import BaseModel, create_model
from .models import CreateInputModel, define_model, Models, STRATEGY_INPUT_MODEL, UpdateInputModel, UpsertInputModel
from .types import FieldDefinition, ResourceSpecification


class Schema(Models):
    _resource_spec: ResourceSpecification

    # def __init_subclass__(cls) -> None:
    #     print('schema __init_subclass__')
    #     return super().__init_subclass__()

    def __init__(self, resource_spec: ResourceSpecification) -> None:
        self._resource_spec = resource_spec

    @staticmethod
    def resolve_spec(resource_spec: ResourceSpecification) -> None:
        for _strategy, _strategy_model in STRATEGY_INPUT_MODEL.items():
            _model_attr: str = f'_{_strategy.lower()}_resource_model'
            _model_name: str = ''.join([k.title() for k in [_strategy, resource_spec.name]])

            _model_definition: BaseModel = define_model(
                base=_strategy_model,
                name=_model_name,
                fields=resource_spec.fields,
                strategy=_strategy)
            self.__setattr__(_model_attr, _model_definition)
