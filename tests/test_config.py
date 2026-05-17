"""Tests for sthali_crud.config."""
import unittest
from unittest.mock import MagicMock

from pydantic import ValidationError

from sthali_crud.config import ConfigSchema, get_app_context, get_context_processors


class TestGetAppContext(unittest.TestCase):

    def test_returns_sthali_as_title(self) -> None:
        mock_request = MagicMock()
        mock_request.app.extra = {}
        result = get_app_context(mock_request)
        self.assertEqual(result["title"], "Sthali")

    def test_returns_crudmodels_from_app_extra(self) -> None:
        mock_request = MagicMock()
        crudmodels = {"items": {"table": "items"}}
        mock_request.app.extra = {"crudmodels": crudmodels}
        result = get_app_context(mock_request)
        self.assertEqual(result["crudmodels"], crudmodels)

    def test_returns_empty_list_when_crudmodels_missing(self) -> None:
        mock_request = MagicMock()
        mock_request.app.extra = {}
        result = get_app_context(mock_request)
        self.assertEqual(result["crudmodels"], [])

    def test_result_contains_title_key(self) -> None:
        mock_request = MagicMock()
        mock_request.app.extra = {}
        result = get_app_context(mock_request)
        self.assertIn("title", result)

    def test_result_contains_crudmodels_key(self) -> None:
        mock_request = MagicMock()
        mock_request.app.extra = {}
        result = get_app_context(mock_request)
        self.assertIn("crudmodels", result)


class TestGetContextProcessors(unittest.TestCase):

    def test_includes_request_object(self) -> None:
        mock_request = MagicMock()
        mock_request.app.extra = {}
        result = get_context_processors(mock_request)
        self.assertIs(result["request"], mock_request)

    def test_includes_title_from_app_context(self) -> None:
        mock_request = MagicMock()
        mock_request.app.extra = {}
        result = get_context_processors(mock_request)
        self.assertIn("title", result)

    def test_includes_crudmodels_from_app_context(self) -> None:
        mock_request = MagicMock()
        crudmodels = {"x": {}}
        mock_request.app.extra = {"crudmodels": crudmodels}
        result = get_context_processors(mock_request)
        self.assertEqual(result["crudmodels"], crudmodels)


class TestConfigSchema(unittest.TestCase):

    def test_validate_with_valid_database_uri(self) -> None:
        data = {"crudmodels": {"database_uri": "sqlite+aiosqlite:///:memory:"}}
        result = ConfigSchema.model_validate(data)
        self.assertEqual(result.crudmodels.database_uri, "sqlite+aiosqlite:///:memory:")

    def test_validate_missing_crudmodels_raises(self) -> None:
        with self.assertRaises(ValidationError):
            ConfigSchema.model_validate({})

    def test_validate_missing_database_uri_raises(self) -> None:
        with self.assertRaises(ValidationError):
            ConfigSchema.model_validate({"crudmodels": {}})

    def test_dependencies_defaults_to_none(self) -> None:
        data = {"crudmodels": {"database_uri": "sqlite:///"}}
        result = ConfigSchema.model_validate(data)
        self.assertIsNone(result.crudmodels.dependencies)

    def test_dependencies_accepts_list_of_strings(self) -> None:
        data = {"crudmodels": {"database_uri": "sqlite:///", "dependencies": ["a", "b"]}}
        result = ConfigSchema.model_validate(data)
        self.assertEqual(result.crudmodels.dependencies, ["a", "b"])

    def test_extra_fields_are_ignored(self) -> None:
        data = {"crudmodels": {"database_uri": "sqlite:///", "unknown_key": "value"}}
        result = ConfigSchema.model_validate(data)
        self.assertIsNotNone(result)


if __name__ == "__main__":
    unittest.main()
