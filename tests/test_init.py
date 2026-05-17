"""Tests for sthali_crud."""
import unittest
from unittest.mock import MagicMock, patch

from sthali_crud import SthaliCRUD, lifespan


class TestLifespan(unittest.IsolatedAsyncioTestCase):

    async def test_lifespan_logs_startup_message(self) -> None:
        mock_app = MagicMock()
        with patch("sthali_crud.logger") as mock_logger:
            async with lifespan(mock_app):
                mock_logger.info.assert_called_with("Database connection successful")

    async def test_lifespan_logs_shutdown_message(self) -> None:
        mock_app = MagicMock()
        with patch("sthali_crud.logger") as mock_logger:
            async with lifespan(mock_app):
                pass
        mock_logger.info.assert_called_with("Application shutting down")

    async def test_lifespan_yields_none(self) -> None:
        mock_app = MagicMock()
        async with lifespan(mock_app) as value:
            self.assertIsNone(value)


class TestSthaliCRUD(unittest.TestCase):

    def setUp(self) -> None:
        engine_patcher = patch("sthali_crud.Engine.load_from_config")
        self.mock_load_engine: MagicMock = engine_patcher.start()
        self.addCleanup(engine_patcher.stop)

        self.mock_config = MagicMock()
        self.mock_config.yaml_config = {
            "crudmodels": {"database_uri": "sqlite+aiosqlite:///:memory:"},
        }

    def _make_definitions(self) -> list:
        mock_model = MagicMock()
        mock_model.__tablename__ = "items"
        return [(mock_model, (MagicMock(), MagicMock(), MagicMock()))]

    def test_init_calls_engine_load_from_config_with_uri(self) -> None:
        with patch.object(SthaliCRUD, "register_api_router", return_value=MagicMock()):
            SthaliCRUD(self.mock_config, [])
        self.mock_load_engine.assert_called_once_with("sqlite+aiosqlite:///:memory:")

    def test_init_stores_dependencies(self) -> None:
        deps: dict[str, MagicMock] = {"api_key": MagicMock()}
        with patch.object(SthaliCRUD, "register_api_router", return_value=MagicMock()):
            crud = SthaliCRUD(self.mock_config, [], dependencies=deps)
        self.assertEqual(crud.dependencies, deps)

    def test_init_stores_definitions(self) -> None:
        definitions = self._make_definitions()
        with patch.object(SthaliCRUD, "register_api_router", return_value=MagicMock()):
            crud = SthaliCRUD(self.mock_config, definitions)
        self.assertEqual(crud.definitions, definitions)

    def test_init_creates_fastapi_app(self) -> None:
        with patch.object(SthaliCRUD, "register_api_router", return_value=MagicMock()):
            crud = SthaliCRUD(self.mock_config, [])
        self.assertIsNotNone(crud.app)

    def test_init_with_empty_definitions_does_not_call_register(self) -> None:
        with patch.object(SthaliCRUD, "register_api_router") as mock_reg:
            SthaliCRUD(self.mock_config, [])
        mock_reg.assert_not_called()

    def test_init_calls_register_once_per_definition(self) -> None:
        definitions = self._make_definitions()
        with patch.object(SthaliCRUD, "register_api_router", return_value=MagicMock()) as mock_reg:
            SthaliCRUD(self.mock_config, definitions)
        self.assertGreaterEqual(mock_reg.call_count, len(definitions))

    def test_init_stores_extended_crudmodels_in_app_extra(self) -> None:
        definitions = self._make_definitions()
        with patch.object(SthaliCRUD, "register_api_router", return_value=MagicMock()):
            crud = SthaliCRUD(self.mock_config, definitions)
        self.assertIn("crudmodels", crud.app.extra)

    def test_init_with_extended_routers_calls_register_extra_times(self) -> None:
        definitions = self._make_definitions()
        mock_ext_router = MagicMock()
        with patch.object(SthaliCRUD, "register_api_router", return_value=MagicMock()) as mock_reg:
            SthaliCRUD(self.mock_config, definitions, extended_routers=[mock_ext_router])
        self.assertGreater(mock_reg.call_count, len(definitions))


if __name__ == "__main__":
    unittest.main()
