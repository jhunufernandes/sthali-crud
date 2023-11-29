from unittest import IsolatedAsyncioTestCase

from src.sthali_crud.db_engines.base import BaseEngine


class TestBaseEngine(IsolatedAsyncioTestCase):
    def setUp(self) -> None:
        self.base_engine = BaseEngine()

    async def test_db_insert_one(self) -> None:
        with self.assertRaises(NotImplementedError):
            await self.base_engine.db_insert_one()

    async def test_db_select_one(self) -> None:
        with self.assertRaises(NotImplementedError):
            await self.base_engine.db_select_one()

    async def test_db_update_one(self) -> None:
        with self.assertRaises(NotImplementedError):
            await self.base_engine.db_update_one()

    async def test_db_delete_one(self) -> None:
        with self.assertRaises(NotImplementedError):
            await self.base_engine.db_delete_one()

    async def test_db_select_all(self) -> None:
        with self.assertRaises(NotImplementedError):
            await self.base_engine.db_select_all()
