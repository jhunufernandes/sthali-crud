from unittest import IsolatedAsyncioTestCase, mock

from src.sthali_crud.db_engines.virtual import HTTPException, VirtualEngine, status
from tests import ID, PAYLOAD_WITH_ID, PAYLOAD_WITHOUT_ID


class TestVirtualEngine(IsolatedAsyncioTestCase):
    def setUp(self):
        db_path = ""
        db_table = "test_table"

        self.virtual_engine = VirtualEngine(db_path, db_table)

    @mock.patch("src.sthali_crud.db_engines.virtual.VirtualEngine.db")
    def test_get(self, mock_db):
        mock_db.__getitem__.return_value = PAYLOAD_WITHOUT_ID

        result = self.virtual_engine._get(ID)
        self.assertEqual(result, PAYLOAD_WITHOUT_ID)

    @mock.patch("src.sthali_crud.db_engines.virtual.VirtualEngine.db")
    def test_get_not_found(self, mock_db):
        mock_db.__getitem__.side_effect = KeyError

        with self.assertRaises(HTTPException) as context:
            self.virtual_engine._get(ID)

        self.assertEqual(context.exception.status_code, status.HTTP_404_NOT_FOUND)

    async def test_db_insert_one(self):
        result = await self.virtual_engine.db_insert_one(ID, PAYLOAD_WITHOUT_ID)
        self.assertEqual(result, PAYLOAD_WITH_ID)

    @mock.patch("src.sthali_crud.db_engines.virtual.VirtualEngine._get")
    async def test_db_select_one(self, mock_get):
        mock_get.return_value = PAYLOAD_WITHOUT_ID

        result = await self.virtual_engine.db_select_one(ID)
        self.assertEqual(result, PAYLOAD_WITH_ID)

    @mock.patch("src.sthali_crud.db_engines.virtual.VirtualEngine._get")
    async def test_db_select_one_not_found(self, mock_get):
        mock_get.side_effect = HTTPException(status.HTTP_404_NOT_FOUND)

        with self.assertRaises(HTTPException) as context:
            await self.virtual_engine.db_select_one(ID)

        self.assertEqual(context.exception.status_code, status.HTTP_404_NOT_FOUND)

    @mock.patch("src.sthali_crud.db_engines.virtual.VirtualEngine._get")
    async def test_db_update_one(self, mock_get):
        mock_get.return_value = PAYLOAD_WITHOUT_ID

        result = await self.virtual_engine.db_update_one(ID, PAYLOAD_WITHOUT_ID)
        self.assertEqual(result, PAYLOAD_WITH_ID)

    @mock.patch("src.sthali_crud.db_engines.virtual.VirtualEngine._get")
    async def test_db_update_one_not_found(self, mock_get):
        mock_get.side_effect = HTTPException(status.HTTP_404_NOT_FOUND)

        with self.assertRaises(HTTPException) as context:
            await self.virtual_engine.db_update_one(ID, PAYLOAD_WITHOUT_ID)

        self.assertEqual(context.exception.status_code, status.HTTP_404_NOT_FOUND)

    @mock.patch("src.sthali_crud.db_engines.virtual.VirtualEngine._get")
    async def test_db_delete_one(self, mock_get):
        mock_get.return_value = PAYLOAD_WITHOUT_ID

        result = await self.virtual_engine.db_delete_one(ID)
        self.assertIsNone(result)

    @mock.patch("src.sthali_crud.db_engines.virtual.VirtualEngine._get")
    async def test_db_delete_one_not_found(self, mock_get):
        mock_get.side_effect = HTTPException(status.HTTP_404_NOT_FOUND)

        with self.assertRaises(HTTPException) as context:
            await self.virtual_engine.db_delete_one(ID)

        self.assertEqual(context.exception.status_code, status.HTTP_404_NOT_FOUND)

    @mock.patch("src.sthali_crud.db_engines.virtual.VirtualEngine.db")
    async def test_db_select_all(self, mock_db):
        mock_db.items.return_value = [(ID, PAYLOAD_WITHOUT_ID)]

        result = await self.virtual_engine.db_select_all()
        self.assertEqual(result, [PAYLOAD_WITH_ID])
