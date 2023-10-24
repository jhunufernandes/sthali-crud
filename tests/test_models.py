from unittest import TestCase
from src.sthali_crud.models import CreateModel, Models, ModelStrategy
from tests import RESOURCE_SPEC


class TestModels(TestCase):
    def setUp(self):
        self._model_fields = set(f.name for f in RESOURCE_SPEC.fields)

    def test_define_model(self) -> None:
        _result = Models.define_model(CreateModel, RESOURCE_SPEC.name, RESOURCE_SPEC.fields)
        assert self._model_fields == set(_result.model_json_schema()['properties'].keys())
        assert _result.model_json_schema()['properties']['name']['type'] == 'string'
        assert 'name' in _result.model_json_schema()['required']
        assert 'people' == _result.model_json_schema()['title']

    def test_resolve_spec(self) -> None:
        _result = Models.resolve_spec(RESOURCE_SPEC)
        assert isinstance(_result, ModelStrategy)
        assert self._model_fields == set(_result.create_model.model_json_schema()['properties'].keys())
        assert self._model_fields.issubset(set(_result.response_model.model_json_schema()['properties'].keys()))
        assert _result.create_model.model_json_schema()['properties']['name']['type'] == 'string'
        assert 'name' in _result.create_model.model_json_schema()['required']
        assert 'CreatePeople' == _result.create_model.model_json_schema()['title']
