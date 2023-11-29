from unittest import IsolatedAsyncioTestCase, mock

from src.sthali_crud.crud import CRUD, CRUDException, status, uuid4
from tests import (
    DB_SPEC,
    FIELD_DEF,
    ID,
    PAYLOAD_WITH_ID,
    PAYLOAD_WITHOUT_ID,
    MockDB,
    MockModels,
)


class TestCRUD(IsolatedAsyncioTestCase):
    def setUp(self):
        db = MockDB(DB_SPEC, "test_table")
        models = MockModels("test_model", [FIELD_DEF])

        self.models = models
        self.crud = CRUD(db, models)

    def test_handle_list(self):
        result_input = [PAYLOAD_WITH_ID]
        response_model = self.models.response_model

        result = self.crud._handle_list(result_input)
        self.assertEqual(result, [response_model(**PAYLOAD_WITH_ID)])

    def test_handle_list_raise_crud_exception_when_assertion_error(self):
        result_input = [{}]

        with self.assertRaises(CRUDException) as context:
            self.crud._handle_list(result_input)

        self.assertEqual(
            context.exception.status_code, status.HTTP_422_UNPROCESSABLE_ENTITY
        )
        self.assertIn("Not found", context.exception.detail)

    def test_handle_list_raise_crud_exception_when_validation_error(self):
        result_input = [PAYLOAD_WITHOUT_ID]

        with self.assertRaises(CRUDException) as context:
            self.crud._handle_list(result_input)

        self.assertEqual(
            context.exception.status_code, status.HTTP_422_UNPROCESSABLE_ENTITY
        )

    def test_handle_result(self):
        response_model = self.models.response_model
        result_input = PAYLOAD_WITH_ID

        result = self.crud._handle_result(result_input)
        self.assertEqual(result, response_model(**PAYLOAD_WITH_ID))

    def test_handle_result_raise_exception_when_assertion_error(self):
        result_input = {}

        with self.assertRaises(CRUDException) as context:
            self.crud._handle_result(result_input)

        self.assertEqual(context.exception.status_code, status.HTTP_404_NOT_FOUND)
        self.assertIn("Not found", context.exception.detail)

    def test_handle_result_raise_exception_when_validation_error(self):
        result_input = PAYLOAD_WITHOUT_ID

        with self.assertRaises(CRUDException) as context:
            self.crud._handle_result(result_input)

        self.assertEqual(
            context.exception.status_code, status.HTTP_422_UNPROCESSABLE_ENTITY
        )

    @mock.patch("src.sthali_crud.crud.CRUD._handle_result")
    async def test_create(self, mock_handle_result):
        mock_handle_result.return_value = PAYLOAD_WITH_ID
        create_model = self.crud.models.create_model

        result = await self.crud.create(create_model(**PAYLOAD_WITHOUT_ID))
        self.assertEqual(result, PAYLOAD_WITH_ID)

    @mock.patch("src.sthali_crud.crud.CRUD._handle_result")
    async def test_read(self, mock_handle_result):
        mock_handle_result.return_value = PAYLOAD_WITH_ID

        result = await self.crud.read(ID)
        self.assertEqual(result, PAYLOAD_WITH_ID)

    @mock.patch("src.sthali_crud.crud.CRUD._handle_result")
    async def test_update_with_id_in_path(self, mock_handle_result):
        mock_handle_result.return_value = PAYLOAD_WITH_ID
        upsert_model = self.crud.models.upsert_model

        result = await self.crud.update(upsert_model(**PAYLOAD_WITHOUT_ID), ID)
        self.assertEqual(result, PAYLOAD_WITH_ID)

    @mock.patch("src.sthali_crud.crud.CRUD._handle_result")
    async def test_update_with_id_in_body(self, mock_handle_result):
        mock_handle_result.return_value = PAYLOAD_WITH_ID
        update_model = self.crud.models.update_model

        result = await self.crud.update(update_model(**PAYLOAD_WITH_ID), ID)
        self.assertEqual(result, PAYLOAD_WITH_ID)

    async def test_update_raise_exception_when_none_id_is_defined(self):
        upsert_model = self.crud.models.upsert_model

        with self.assertRaises(CRUDException) as context:
            await self.crud.update(upsert_model(**PAYLOAD_WITHOUT_ID))

        self.assertEqual(context.exception.status_code, status.HTTP_404_NOT_FOUND)
        self.assertIn("None id is defined", context.exception.detail)

    async def test_update_raise_exception_when_ids_cant_match(self):
        update_model = self.crud.models.update_model
        _id = uuid4()

        with self.assertRaises(CRUDException) as context:
            await self.crud.update(update_model(**PAYLOAD_WITH_ID), _id)

        self.assertEqual(context.exception.status_code, status.HTTP_404_NOT_FOUND)
        self.assertIn("Ids cant match", context.exception.detail)

    async def test_delete(self):
        result = await self.crud.delete(ID)
        self.assertIsNone(result)

    async def test_delete_raise_exception_when_result_is_not_none(self):
        self.crud.db.delete = mock.AsyncMock(return_value=PAYLOAD_WITH_ID)

        with self.assertRaises(CRUDException) as context:
            await self.crud.delete(ID)

        self.assertEqual(
            context.exception.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR
        )
        self.assertIn("Result is not none", context.exception.detail)

    @mock.patch("src.sthali_crud.crud.CRUD._handle_list")
    async def test_read_all(self, mock_handle_list):
        response_model = self.crud.response_model
        mock_handle_list.return_value = [response_model(**PAYLOAD_WITH_ID)]

        result = await self.crud.read_all()
        self.assertEqual(result, [response_model(**PAYLOAD_WITH_ID)])
