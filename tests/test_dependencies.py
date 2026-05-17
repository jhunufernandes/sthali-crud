"""Tests for sthali_crud.dependencies."""
import unittest

from pydantic import ValidationError

from sthali_crud.dependencies import PaginateParameters


class TestPaginateParameters(unittest.TestCase):

    def test_default_skip_is_zero(self) -> None:
        result = PaginateParameters.model_validate({})
        self.assertEqual(result.skip, 0)

    def test_default_limit_is_100(self) -> None:
        result = PaginateParameters.model_validate({})
        self.assertEqual(result.limit, 100)

    def test_custom_skip_accepted(self) -> None:
        result = PaginateParameters.model_validate({"skip": 25})
        self.assertEqual(result.skip, 25)

    def test_custom_limit_accepted(self) -> None:
        result = PaginateParameters.model_validate({"limit": 10})
        self.assertEqual(result.limit, 10)

    def test_both_custom_values_accepted(self) -> None:
        result = PaginateParameters.model_validate({"skip": 5, "limit": 20})
        self.assertEqual(result.skip, 5)
        self.assertEqual(result.limit, 20)

    def test_negative_skip_raises_validation_error(self) -> None:
        with self.assertRaises(ValidationError):
            PaginateParameters.model_validate({"skip": -1})

    def test_negative_limit_raises_validation_error(self) -> None:
        with self.assertRaises(ValidationError):
            PaginateParameters.model_validate({"limit": -1})

    def test_zero_skip_is_valid(self) -> None:
        result = PaginateParameters.model_validate({"skip": 0})
        self.assertEqual(result.skip, 0)

    def test_zero_limit_is_valid(self) -> None:
        result = PaginateParameters.model_validate({"limit": 0})
        self.assertEqual(result.limit, 0)

    def test_large_values_accepted(self) -> None:
        result = PaginateParameters.model_validate({"skip": 10000, "limit": 10000})
        self.assertEqual(result.skip, 10000)
        self.assertEqual(result.limit, 10000)


if __name__ == "__main__":
    unittest.main()
