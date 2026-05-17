"""Tests for sthali_crud.routers."""
import unittest
from unittest.mock import MagicMock, patch

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel as PydanticBaseModel
from pydantic import ValidationError

from sthali_crud.routers import Base


class _DummyModel(PydanticBaseModel):
    x: int


class ConcreteRouter(Base):
    prefix = "/test"

    @property
    def api_router(self) -> APIRouter:
        return APIRouter()


class TestBase(unittest.TestCase):

    def setUp(self) -> None:
        self.mock_db_session = MagicMock()
        self.mock_model = MagicMock()
        self.mock_model.__tablename__ = "items"
        self.mock_create_schema = MagicMock()
        self.mock_read_schema = MagicMock()
        self.mock_update_schema = MagicMock()
        self.router = ConcreteRouter(
            self.mock_db_session,
            self.mock_model,
            self.mock_create_schema,
            self.mock_read_schema,
            self.mock_update_schema,
        )
        # Build a real ValidationError for 422-path tests
        self.sample_ve: ValidationError | None = None
        try:
            _DummyModel.model_validate({"x": "not-an-int"})
        except ValidationError as e:
            self.sample_ve = e

    def test_init_stores_db_session(self) -> None:
        self.assertIs(self.router.db_session, self.mock_db_session)

    def test_init_stores_model(self) -> None:
        self.assertIs(self.router.model, self.mock_model)

    def test_init_stores_read_schema(self) -> None:
        self.assertIs(self.router.read_schema, self.mock_read_schema)

    def test_init_stores_create_schema(self) -> None:
        self.assertIs(self.router.create_schema, self.mock_create_schema)

    def test_init_stores_update_schema(self) -> None:
        self.assertIs(self.router.update_schema, self.mock_update_schema)

    def test_prefix_class_var_is_none_on_base(self) -> None:
        self.assertIsNone(Base.prefix)

    def test_api_router_raises_not_implemented_on_base(self) -> None:
        bare = Base.__new__(Base)
        with self.assertRaises(NotImplementedError):
            _ = bare.api_router

    def test_resource_name_returns_tablename(self) -> None:
        self.assertEqual(self.router.resource_name, "items")

    def test_handle_result_raises_404_when_result_is_none(self) -> None:
        with self.assertRaises(HTTPException) as ctx:
            self.router.handle_result(None)
        self.assertEqual(ctx.exception.status_code, 404)

    def test_handle_result_raises_404_when_result_is_falsy(self) -> None:
        with self.assertRaises(HTTPException) as ctx:
            self.router.handle_result(MagicMock(__bool__=lambda _s: False))
        self.assertEqual(ctx.exception.status_code, 404)

    def test_handle_result_returns_validated_schema(self) -> None:
        mock_result = MagicMock()
        mock_validated = MagicMock()
        self.mock_read_schema.model_validate.return_value = mock_validated
        result = self.router.handle_result(mock_result)
        self.assertIs(result, mock_validated)

    def test_handle_result_calls_model_validate_with_result(self) -> None:
        mock_result = MagicMock()
        self.router.handle_result(mock_result)
        self.mock_read_schema.model_validate.assert_called_once_with(mock_result)

    def test_handle_result_raises_422_on_validation_error(self) -> None:
        self.assertIsNotNone(self.sample_ve)
        mock_result = MagicMock()
        self.mock_read_schema.model_validate.side_effect = self.sample_ve
        with self.assertRaises(HTTPException) as ctx:
            self.router.handle_result(mock_result)
        self.assertEqual(ctx.exception.status_code, 422)

    def test_handle_list_result_returns_empty_list_for_empty_input(self) -> None:
        result = self.router.handle_list_result([])
        self.assertEqual(result, [])

    def test_handle_list_result_returns_all_valid_items(self) -> None:
        mock_items = [MagicMock(), MagicMock()]
        validated = [MagicMock(), MagicMock()]
        self.mock_read_schema.model_validate.side_effect = validated
        result = self.router.handle_list_result(mock_items)
        self.assertEqual(len(result), 2)

    def test_handle_list_result_raises_400_when_any_item_invalid(self) -> None:
        mock_items = [MagicMock()]
        with patch.object(self.router, "handle_result", side_effect=HTTPException(404, "x")), \
                self.assertRaises(HTTPException) as ctx:
            self.router.handle_list_result(mock_items)
        self.assertEqual(ctx.exception.status_code, 400)

    def test_handle_list_result_collects_all_errors_before_raising(self) -> None:
        mock_items = [MagicMock(), MagicMock()]
        with patch.object(self.router, "handle_result", side_effect=HTTPException(404, "x")), \
                self.assertRaises(HTTPException) as ctx:
            self.router.handle_list_result(mock_items)
        self.assertIsInstance(ctx.exception.detail, list)
        self.assertEqual(len(ctx.exception.detail), 2)


if __name__ == "__main__":
    unittest.main()
