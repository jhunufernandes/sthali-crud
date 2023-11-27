from unittest import TestCase

# from src.sthali_crud.models import Base, Models
from src.sthali_crud.models import Models
from tests import RESOURCE_SPEC


class TestModels(TestCase):
    def setUp(self):
        self.models = Models("people", RESOURCE_SPEC.fields)

    def test_class(self):
        assert self.models.name == "people"

    # def test_define_model(self):
    #     result = Models.define_model(Base, 'people', RESOURCE_SPEC.fields)
