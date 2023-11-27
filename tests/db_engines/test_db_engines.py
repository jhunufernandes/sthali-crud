from unittest import IsolatedAsyncioTestCase, mock

from src.sthali_crud.db_engines import DBEngine, DBSpecification, BaseEngine


class MockEngine(BaseEngine):
    db_insert_one = mock.AsyncMock(return_value={})
    db_select_one = mock.AsyncMock(return_value={})
    db_update_one = mock.AsyncMock(return_value={})
    db_delete_one = mock.AsyncMock(return_value={})
    db_select_all = mock.AsyncMock(return_value={})


class TestDBEngine(IsolatedAsyncioTestCase):
    def setUp(self) -> None:
        engine = "postgres"
        path = "mock_path"
        table = "mock_table"

        db_spec = DBSpecification(engine=engine, path=path)
        db_engine = DBEngine(db_spec=db_spec, table=table)
        db_engine.engine = MockEngine
        self.db_engine = db_engine

    async def test_db_insert_one(self) -> None:
        result = await self.db_engine.db_insert_one()
        self.assertEqual(result, {})

    async def test_db_select_one(self) -> None:
        result = await self.db_engine.db_select_one()
        self.assertEqual(result, {})

    async def test_db_update_one(self) -> None:
        result = await self.db_engine.db_update_one()
        self.assertEqual(result, {})

    async def test_db_delete_one(self) -> None:
        result = await self.db_engine.db_delete_one()
        self.assertEqual(result, {})

    async def test_db_select_all(self) -> None:
        result = await self.db_engine.db_select_all()
        self.assertEqual(result, {})
