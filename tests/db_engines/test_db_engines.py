from unittest import IsolatedAsyncioTestCase

from src.sthali_crud.db_engines import DBEngine, DBSpecification
from tests import DB_SPEC, ID, PAYLOAD_WITH_ID, PAYLOAD_WITHOUT_ID


class TestDBEngine(IsolatedAsyncioTestCase):
    def setUp(self) -> None:
        engine = "virtual"
        path = DB_SPEC.path
        db_spec = DBSpecification(engine=engine, path=path)
        table = "test_table"

        self.db_engine = DBEngine(db_spec=db_spec, table=table)

    async def test_db_insert_one(self) -> None:
        result = await self.db_engine.db_insert_one(ID, PAYLOAD_WITHOUT_ID)
        self.assertEqual(result, PAYLOAD_WITH_ID)

    async def test_db_select_one(self) -> None:
        await self.db_engine.db_insert_one(ID, PAYLOAD_WITHOUT_ID)

        result = await self.db_engine.db_select_one(ID)
        self.assertEqual(result, PAYLOAD_WITH_ID)

    async def test_db_update_one(self) -> None:
        await self.db_engine.db_insert_one(ID, PAYLOAD_WITHOUT_ID)

        NEW_PAYLOAD = PAYLOAD_WITH_ID.copy()
        NEW_PAYLOAD["field_1"] = "new_value"
        result = await self.db_engine.db_update_one(ID, NEW_PAYLOAD)
        self.assertEqual(result, NEW_PAYLOAD)

    async def test_db_delete_one(self) -> None:
        await self.db_engine.db_insert_one(ID, PAYLOAD_WITHOUT_ID)

        result = await self.db_engine.db_delete_one(ID)
        self.assertIsNone(result)

    async def test_db_select_all(self) -> None:
        result = await self.db_engine.db_select_all()
        self.assertEqual(result, [PAYLOAD_WITH_ID])
