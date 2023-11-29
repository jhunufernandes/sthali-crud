from unittest import TestCase

from src.sthali_crud.models import UUID, BaseModel, Models
from tests import RESOURCE_SPEC, PAYLOAD_WITHOUT_ID, PAYLOAD_WITH_ID


class TestModels(TestCase):
    def setUp(self):
        name = "test_model"
        fields = RESOURCE_SPEC.fields

        self.models = Models(name, fields)

    def test_create_model_fields(self):
        create_model = self.models.create_model

        result = create_model(**PAYLOAD_WITHOUT_ID)
        self.assertNotIn("id", create_model.model_fields)
        self.assertIsInstance(result, create_model)

    def test_response_model_fields(self):
        response_model = self.models.response_model

        result = response_model(**PAYLOAD_WITH_ID)
        self.assertIn("id", response_model.model_fields)
        self.assertEqual(response_model.model_fields["id"].annotation, UUID)
        self.assertIsInstance(result, response_model)

    def test_update_model_fields(self):
        update_model = self.models.update_model

        result = update_model(**PAYLOAD_WITH_ID)
        self.assertIn("id", update_model.model_fields)
        self.assertEqual(update_model.model_fields["id"].annotation, UUID)
        self.assertIsInstance(result, update_model)

    def test_upsert_model_fields(self):
        upsert_model = self.models.upsert_model

        result = upsert_model(**PAYLOAD_WITH_ID)
        result_without_id = upsert_model(**PAYLOAD_WITHOUT_ID)
        self.assertIn("id", upsert_model.model_fields)
        self.assertEqual(upsert_model.model_fields["id"].annotation, UUID | None)
        self.assertIsInstance(result, upsert_model)
        self.assertIsInstance(result_without_id, upsert_model)

    def test_define_model(self):
        base = BaseModel
        name = "test_model"
        fields = RESOURCE_SPEC.fields
        model = Models.define_model(base, name, fields)

        result = model(**PAYLOAD_WITHOUT_ID)
        self.assertIsNotNone(result)
        self.assertIsInstance(result, model)
