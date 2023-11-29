# from unittest import IsolatedAsyncioTestCase, mock
# # from uuid import uuid4

# from src.sthali_crud.db_engines.postgres import (
#     PostgresEngine
# )


# class TestTinyDBEngine(IsolatedAsyncioTestCase):
#     def setUp(self):
#         self.db_path = ""
#         self.db_table = "test_table"

#         # with mock.patch("src.sthali_crud.db_engines.tinydb.TinyDB") as mock_tiny_db:
#         #     # mock_tiny_db.return_value = MockTinyDB
#         #     postgres_engine = PostgresEngine(self.db_path, self.db_table)
#         #     self.postgres_engine = postgres_engine

#     # def test_get(self):
#     #     resource_id = uuid4()

#     #     self.tiny_db_engine.db.table.return_value.search.return_value = [{}]

#     #     result = self.tiny_db_engine._get(resource_id)
#     #     self.assertEqual(result, {})

#     # def test_get_not_found(self):
#     #     resource_id = uuid4()

#     #     self.tiny_db_engine.db.table.return_value.search.return_value = []

#     #     with self.assertRaises(HTTPException) as context:
#     #         self.tiny_db_engine._get(resource_id)

#     #     self.assertEqual(context.exception.status_code, status.HTTP_404_NOT_FOUND)

#     # def test_get_not_found_without_raise(self):
#     #     resource_id = uuid4()

#     #     self.tiny_db_engine.db.table.return_value.search.return_value = [{}]

#     #     with self.assertRaises(HTTPException) as context:
#     #         self.tiny_db_engine._get(resource_id, False)

#     #     self.assertEqual(context.exception.status_code, status.HTTP_404_NOT_FOUND)

#     # async def test_db_insert_one(self):
#     #     resource_id = uuid4()
#     #     resource_obj = {"key": "value"}

#     #     result = await self.tiny_db_engine.db_insert_one(resource_id, resource_obj)
#     #     self.assertEqual(result, {"id": str(resource_id), **resource_obj})

#     # @mock.patch("src.sthali_crud.db_engines.tinydb.TinyDBEngine._get")
#     # async def test_db_select_one(self, mock_get):
#     #     resource_id = uuid4()
#     #     resource_obj = {"key": "value"}

#     #     mock_get.return_value = {"id": resource_id, "resource_obj": resource_obj}

#     #     result = await self.tiny_db_engine.db_select_one(resource_id)
#     #     self.assertEqual(result, {"id": str(resource_id), **resource_obj})

#     # async def test_db_select_one_not_found(self):
#     #     resource_id = uuid4()

#     #     self.tiny_db_engine.db.table.return_value.search.return_value = None

#     #     with self.assertRaises(HTTPException) as context:
#     #         await self.tiny_db_engine.db_select_one(resource_id)

#     #     self.assertEqual(context.exception.status_code, status.HTTP_404_NOT_FOUND)

#     # @mock.patch("src.sthali_crud.db_engines.tinydb.TinyDBEngine._get")
#     # async def test_db_update_one(self, mock_get):
#     #     resource_id = uuid4()
#     #     updated_obj = {"new_key": "new_value"}

#     #     mock_get.return_value = {}

#     #     result = await self.tiny_db_engine.db_update_one(resource_id, updated_obj)
#     #     self.assertEqual(result, {"id": str(resource_id), **updated_obj})

#     # async def test_db_update_one_not_found(self):
#     #     resource_id = uuid4()
#     #     resource_obj = {"new_key": "new_value"}

#     #     self.tiny_db_engine.db.table.return_value.search.return_value = None

#     #     with self.assertRaises(HTTPException) as context:
#     #         await self.tiny_db_engine.db_update_one(resource_id, resource_obj)

#     #     self.assertEqual(context.exception.status_code, status.HTTP_404_NOT_FOUND)

#     # @mock.patch("src.sthali_crud.db_engines.tinydb.TinyDBEngine._get")
#     # async def test_db_delete_one(self, mock_get):
#     #     resource_id = uuid4()

#     #     mock_get.return_value = {}

#     #     result = await self.tiny_db_engine.db_delete_one(resource_id)
#     #     self.assertIsNone(result)

#     # async def test_db_delete_one_not_found(self):
#     #     resource_id = uuid4()

#     #     self.tiny_db_engine.db.table.return_value.search.return_value = None

#     #     with self.assertRaises(HTTPException) as context:
#     #         await self.tiny_db_engine.db_delete_one(resource_id)

#     #     self.assertEqual(context.exception.status_code, status.HTTP_404_NOT_FOUND)

#     # async def test_db_select_all(self):
#     #     records = [
#     #         {"resource_id": str(uuid4()), "resource_obj": {"key": "value1"}},
#     #         {"resource_id": str(uuid4()), "resource_obj": {"key": "value2"}},
#     #     ]

#     #     self.tiny_db_engine.db.table.return_value.all.return_value = records
#     #     expected_result = [
#     #         {"id": record["resource_id"], **record["resource_obj"]}
#     #         for record in records
#     #     ]

#     #     result = await self.tiny_db_engine.db_select_all()
#     #     self.assertEqual(result, expected_result)
