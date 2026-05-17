"""Tests for sthali_crud.routers.api."""
import unittest
from collections.abc import Callable
from typing import Any
from unittest.mock import MagicMock
from uuid import UUID

from fastapi import APIRouter
from sthali_db import BaseSchema

from sthali_crud.routers.api import API, replace_type_hint


class _ItemCreateSchema(BaseSchema):
    name: str


class _ItemReadSchema(_ItemCreateSchema):
    id: UUID


class _ItemUpdateSchema(_ItemCreateSchema):
    pass


class TestReplaceTypeHint(unittest.TestCase):

    def test_replaces_annotation_when_type_name_present(self) -> None:
        def func(resource: str) -> None:
            pass

        new_type = MagicMock()
        replace_type_hint(func, "resource", new_type)
        self.assertIs(func.__annotations__["resource"], new_type)

    def test_returns_the_same_function_object(self) -> None:
        def func(resource: str) -> None:
            pass

        result = replace_type_hint(func, "resource", MagicMock())
        self.assertIs(result, func)

    def test_does_not_modify_annotations_when_type_name_absent(self) -> None:
        def func(other: str) -> None:
            pass

        original_annotations = dict(func.__annotations__)
        replace_type_hint(func, "resource", MagicMock())
        self.assertEqual(func.__annotations__, original_annotations)

    def test_no_error_when_function_has_no_annotations(self) -> None:
        def func() -> None:  # type: ignore[return]
            pass

        result = replace_type_hint(func, "resource", MagicMock())
        self.assertIs(result, func)


class TestAPI(unittest.TestCase):

    def setUp(self) -> None:
        self.mock_db_session = MagicMock()
        self.mock_model = MagicMock()
        self.mock_model.__tablename__ = "items"
        self.api = API(
            self.mock_db_session,
            self.mock_model,
            _ItemCreateSchema,
            _ItemReadSchema,
            _ItemUpdateSchema,
        )

    def test_prefix_is_api_v1(self) -> None:
        self.assertEqual(API.prefix, "/api/v1")

    def test_local_context_contains_create_url(self) -> None:
        self.assertIn("url_for_api_create", self.api.local_context)

    def test_local_context_contains_read_url(self) -> None:
        self.assertIn("url_for_api_read", self.api.local_context)

    def test_local_context_contains_update_url(self) -> None:
        self.assertIn("url_for_api_update", self.api.local_context)

    def test_local_context_contains_delete_url(self) -> None:
        self.assertIn("url_for_api_delete", self.api.local_context)

    def test_local_context_contains_read_many_url(self) -> None:
        self.assertIn("url_for_api_read_many", self.api.local_context)

    def test_local_context_names_include_resource_name(self) -> None:
        context = self.api.local_context
        self.assertIn("items", context["url_for_api_create"])

    def test_create_endpoint_returns_callable(self) -> None:
        self.assertIsInstance(self.api.create_endpoint, Callable)

    def test_read_endpoint_returns_callable(self) -> None:
        self.assertIsInstance(self.api.read_endpoint, Callable)

    def test_update_endpoint_returns_callable(self) -> None:
        self.assertIsInstance(self.api.update_endpoint, Callable)

    def test_delete_endpoint_returns_callable(self) -> None:
        self.assertIsInstance(self.api.delete_endpoint, Callable)

    def test_read_many_endpoint_returns_callable(self) -> None:
        self.assertIsInstance(self.api.read_many_endpoint, Callable)

    def test_api_router_returns_api_router_instance(self) -> None:
        result = self.api.api_router
        self.assertIsInstance(result, APIRouter)

    def test_api_router_prefix_includes_tablename(self) -> None:
        router = self.api.api_router
        self.assertIn("items", router.prefix)

    def test_api_router_has_multiple_routes(self) -> None:
        router = self.api.api_router
        self.assertGreater(len(router.routes), 0)

    def test_resource_name_is_tablename(self) -> None:
        self.assertEqual(self.api.resource_name, "items")

    def test_each_endpoint_property_returns_independent_callable(self) -> None:
        ep1: Callable[..., Any] = self.api.create_endpoint
        ep2: Callable[..., Any] = self.api.create_endpoint
        # Each property call returns a new closure
        self.assertIsNot(ep1, ep2)


if __name__ == "__main__":
    unittest.main()
