from unittest import IsolatedAsyncioTestCase, mock

from src.sthali_crud.db_engines.tinydb import TinyDBEngine, HTTPException, status
from tests import ID, PAYLOAD_WITH_ID, PAYLOAD_WITHOUT_ID, db_engines


class TestTinyDBEngine(IsolatedAsyncioTestCase):
    def setUp(self):
        db_path = "test_db.json"
        db_table = "test_table"

        with mock.patch("src.sthali_crud.db_engines.tinydb.TinyDB") as mock_tiny_db:
            mock_tiny_db.return_value = db_engines.MockTinyDB
            tiny_db_engine = TinyDBEngine(db_path, db_table)
            tiny_db_engine.db.table = mock.Mock()
            self.tiny_db_engine = tiny_db_engine

    def test_get(self):
        self.tiny_db_engine.db.table.return_value.search.return_value = [
            PAYLOAD_WITHOUT_ID
        ]

        result = self.tiny_db_engine._get(ID)
        self.assertEqual(result, PAYLOAD_WITHOUT_ID)

    def test_get_not_found(self):
        self.tiny_db_engine.db.table.return_value.search.return_value = []

        with self.assertRaises(HTTPException) as context:
            self.tiny_db_engine._get(ID)

        self.assertEqual(context.exception.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_not_found_without_raise(self):
        self.tiny_db_engine.db.table.return_value.search.return_value = [{}]

        result = self.tiny_db_engine._get(ID, False)
        self.assertEqual(result, {})

    async def test_db_insert_one(self):
        result = await self.tiny_db_engine.db_insert_one(ID, PAYLOAD_WITHOUT_ID)
        self.assertEqual(result, PAYLOAD_WITH_ID)

    @mock.patch("src.sthali_crud.db_engines.tinydb.TinyDBEngine._get")
    async def test_db_select_one(self, mock_get):
        mock_get.return_value = {"resource_obj": PAYLOAD_WITHOUT_ID}

        result = await self.tiny_db_engine.db_select_one(ID)
        self.assertEqual(result, PAYLOAD_WITH_ID)

    async def test_db_select_one_not_found(self):
        self.tiny_db_engine.db.table.return_value.search.return_value = []

        with self.assertRaises(HTTPException) as context:
            await self.tiny_db_engine.db_select_one(ID)

        self.assertEqual(context.exception.status_code, status.HTTP_404_NOT_FOUND)

    @mock.patch("src.sthali_crud.db_engines.tinydb.TinyDBEngine._get")
    async def test_db_update_one(self, mock_get):
        mock_get.return_value = {"resource_obj": PAYLOAD_WITHOUT_ID}

        result = await self.tiny_db_engine.db_update_one(ID, PAYLOAD_WITHOUT_ID)
        self.assertEqual(result, PAYLOAD_WITH_ID)

    async def test_db_update_one_not_found(self):
        self.tiny_db_engine.db.table.return_value.search.return_value = []

        with self.assertRaises(HTTPException) as context:
            await self.tiny_db_engine.db_update_one(ID, PAYLOAD_WITHOUT_ID)

        self.assertEqual(context.exception.status_code, status.HTTP_404_NOT_FOUND)

    @mock.patch("src.sthali_crud.db_engines.tinydb.TinyDBEngine._get")
    async def test_db_delete_one(self, mock_get):
        mock_get.return_value = {"resource_obj": PAYLOAD_WITHOUT_ID}

        result = await self.tiny_db_engine.db_delete_one(ID)
        self.assertIsNone(result)

    async def test_db_delete_one_not_found(self):
        self.tiny_db_engine.db.table.return_value.search.return_value = None

        with self.assertRaises(HTTPException) as context:
            await self.tiny_db_engine.db_delete_one(ID)

        self.assertEqual(context.exception.status_code, status.HTTP_404_NOT_FOUND)

    async def test_db_select_all(self):
        records = [{"resource_id": ID, "resource_obj": PAYLOAD_WITHOUT_ID}]
        self.tiny_db_engine.db.table.return_value.all.return_value = records

        result = await self.tiny_db_engine.db_select_all()
        self.assertEqual(result, [PAYLOAD_WITH_ID])
