from unittest import TestCase
from src.sthali_crud.config import Config
from src.sthali_crud.types import RouteConfiguration, RouterConfiguration
from tests import MockCRUD, MockDB, MockModels, RESOURCE_SPEC


class TestConfig(TestCase):
    def setUp(self) -> None:
        _db = MockDB()
        self._models = MockModels(RESOURCE_SPEC)
        self._crud = MockCRUD(_db, self._models)

    def test_replace_type_hint(self) -> None:
        def func(x: int) -> float:
            return float(x)

        _result = Config.replace_type_hint(func, 'x', str)
        assert _result.__annotations__['x'] == str

    def test_config_router(self) -> None:
        _result = Config.config_router(self._crud, self._models, RESOURCE_SPEC)
        assert isinstance(_result, RouterConfiguration)
        assert _result.prefix == '/people'
        assert isinstance(_result.routes[0], RouteConfiguration)
        assert _result.tags == ['people']
