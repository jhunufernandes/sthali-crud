from unittest import TestCase, IsolatedAsyncioTestCase, mock

from src.sthali_crud.config import (
    default_lifespan, FastAPI, replace_type_hint, ConfigException, load_and_parse_spec_file, config_router, get_type, load_spec_file, Types
)
from tests import DB_SPEC, FIELD_DEF, MockCRUD, MockDB, MockModels, RESOURCE_SPEC


class TestDefaultLifespan(IsolatedAsyncioTestCase):
    async def test_default_lifespan(self):
        app = FastAPI()

        with self.assertLogs() as logs:
            async with default_lifespan(app):
                self.assertIn("Startup SthaliCRUD", logs.output[-1])

            self.assertIn("Shutdown SthaliCRUD", logs.output[-1])


class TestReplaceTypeHint(TestCase):
    def test_replace_type_hint(self):
        def original_func(param: int) -> str:
            return str(param)

        result = replace_type_hint(original_func, 'param', float)
        self.assertEqual(result.__annotations__['param'], float)

    def test_replace_type_hint_non_existing_annotation(self):
        def original_func(param: int) -> str:
            return str(param)

        result = replace_type_hint(original_func, 'non_existing_param', float)
        self.assertEqual(result, original_func)

    def test_replace_type_hint_no_annotations(self):
        def original_func(param) -> str:
            return str(param)

        result = replace_type_hint(original_func, 'param', float)
        self.assertEqual(result, original_func)


class TestGetType(TestCase):
    def test_get_type(self):
        type_str = 'int'

        result = get_type(type_str)
        self.assertEqual(result, Types.int)

    def test_get_type_invalid_type(self):
        type_str = 'nonexistenttype'

        with self.assertRaises(ConfigException) as context:
            get_type(type_str)

        self.assertEqual(str(context.exception), "Invalid type")

    def test_get_type_case_insensitivity(self):
        type_str = 'Int'

        result = get_type(type_str)
        self.assertEqual(result, Types.int)


class TestLoadSpecFile(TestCase):
    def test_load_spec_file_json(self):
        file_path = 'test.json'
        file_content = '{"key": "value"}'

        with mock.patch('builtins.open', mock.mock_open(read_data=file_content)):
            result = load_spec_file(file_path)

        self.assertEqual(result, {'key': 'value'})

    def test_load_spec_file_yaml(self):
        file_path = 'test.yaml'
        file_content = 'key: value'

        with mock.patch('builtins.open', mock.mock_open(read_data=file_content)):
            result = load_spec_file(file_path)

        self.assertEqual(result, {'key': 'value'})

    def test_load_spec_file_raise_exception_when_invalid_extension(self):
        file_path = 'test.txt'

        with self.assertRaises(ConfigException) as context:
            load_spec_file(file_path)

        self.assertEqual(str(context.exception), "Invalid file extension")


class TestConfigRouter(TestCase):
    def test_config_router(self) -> None:
        db = MockDB(DB_SPEC, "test_table")
        models = MockModels("test_model", [FIELD_DEF])
        crud = MockCRUD(db, models)

        result = config_router(crud, RESOURCE_SPEC.name, models)
        self.assertEqual(result.prefix, "/test_resource")
        self.assertEqual(result.tags, ["test_resource"])


class TestLoadAndParseSpecFile(TestCase):
    @mock.patch('src.sthali_crud.config.load_spec_file')
    @mock.patch('src.sthali_crud.config.get_type')
    def test_load_and_parse_spec_file_json(self, mocked_get_type, mocked_load_spec_file):
        mocked_get_type.return_value = int
        mocked_load_spec_file.return_value = {'resources': [{'fields': [{'type': 'int'}]}]}
        file_path = 'test.json'

        result = load_and_parse_spec_file(file_path)
        self.assertEqual(result, {'resources': [{'fields': [{'type': int}]}]})

    @mock.patch('src.sthali_crud.config.load_spec_file')
    @mock.patch('src.sthali_crud.config.get_type')
    def test_load_and_parse_spec_file_yaml(self, mocked_get_type, mocked_load_spec_file):
        mocked_get_type.return_value = int
        mocked_load_spec_file.return_value = {'resources': [{'fields': [{'type': 'int'}]}]}
        file_path = 'test.yaml'

        result = load_and_parse_spec_file(file_path)
        self.assertEqual(result, {'resources': [{'fields': [{'type': int}]}]})

    @mock.patch('src.sthali_crud.config.load_spec_file')
    def test_load_and_parse_spec_file_raise_exception_when_invalid_field_type(self, mocked_load_spec_file):
        mocked_load_spec_file.return_value = {'resources': [{'fields': [{'type': ()}]}]}
        file_path = 'test.yaml'

        with self.assertRaises(ConfigException) as context:
            load_and_parse_spec_file(file_path)

        self.assertEqual(str(context.exception), "Invalid field type")

    def test_load_and_parse_spec_file_raise_exception_when_invalid_file_extension(self):
        file_path = 'test.txt'

        with self.assertRaises(ConfigException) as context:
            load_and_parse_spec_file(file_path)

        self.assertEqual(str(context.exception), "Invalid file extension")
