from unittest import IsolatedAsyncioTestCase, mock

from src.sthali_crud.db import DB
from tests import ID, db_engines, PAYLOAD_WITHOUT_ID, PAYLOAD_WITH_ID


class TestDB(IsolatedAsyncioTestCase):
    def setUp(self):
        with mock.patch("src.sthali_crud.db.DBEngine") as mock_db_engine:
            mock_db_engine.return_value = db_engines.MockDBEngine
            db = DB.__new__(DB)
            db.engine = db_engines.MockEngine
            self.db = db

    async def test_create(self):
        result = await self.db.create(ID, PAYLOAD_WITHOUT_ID)
        self.assertEqual(result, PAYLOAD_WITH_ID)

    async def test_read(self):
        result = await self.db.read(ID)
        self.assertEqual(result, PAYLOAD_WITH_ID)

    async def test_update(self):
        result = await self.db.update(ID, PAYLOAD_WITHOUT_ID)
        self.assertEqual(result, PAYLOAD_WITH_ID)

    async def test_delete(self):
        result = await self.db.delete(ID)
        self.assertIsNone(result)

    async def test_read_all(self):
        result = await self.db.read_all()
        self.assertEqual(result, [PAYLOAD_WITH_ID])
