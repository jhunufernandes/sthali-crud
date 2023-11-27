from unittest import TestCase

from src.sthali_crud.config import (
    config_router,
    replace_type_hint,
    load_and_parse_spec_file,
    ConfigException,
)
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

        _result = replace_type_hint(func, "x", str)
        assert _result.__annotations__["x"] == str

    def test_replace_type_hint_return_same_func_when_type_name_is_not_in_annotations(
        self
    ) -> None:
        def func(y: int) -> float:
            return float(y)

        _result = replace_type_hint(func, "x", str)
        with self.assertRaises(KeyError):
            assert _result.__annotations__["x"] == str

    def test_config_router(self) -> None:
        result = config_router(self.crud, RESOURCE_SPEC.name, self.models)
        assert isinstance(result, RouterConfiguration)
        assert result.prefix == "/people"
        assert isinstance(result.routes[0], RouteConfiguration)
        assert result.tags == ["people"]

    def test_load_and_parse_spec_file(self) -> None:
        # result = parse_spec_file()
        pass

    def test_load_and_parse_spec_file_raise_config_exception_when_spec_file_extension_is_invalid(
        self
    ) -> None:
        spec_file_path = "spec_file.xml"

        with self.assertRaises(ConfigException):
            load_and_parse_spec_file(spec_file_path)
