from unittest import TestCase

from src.sthali_crud.config import config_router, replace_type_hint
from tests import (
    RESOURCE_SPEC,
    MockCRUD,
    MockModels,
    RouteConfiguration,
    RouterConfiguration,
)


class TestConfig(TestCase):
    def setUp(self) -> None:
        self.crud = MockCRUD
        self.models = MockModels

    def test_replace_type_hint(self) -> None:
        def func(x: int) -> float:
            return float(x)

        _result = replace_type_hint(func, 'x', str)
        assert _result.__annotations__['x'] == str

    def test_config_router(self) -> None:
        result = config_router(self.crud, RESOURCE_SPEC.name, self.models)
        assert isinstance(result, RouterConfiguration)
        assert result.prefix == "/people"
        assert isinstance(result.routes[0], RouteConfiguration)
        assert result.tags == ["people"]
