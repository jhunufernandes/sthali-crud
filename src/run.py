import os

from spec_example import EXAMPLE_SPEC
from sthali_crud import AppSpecification, SthaliCRUD, load_and_parse_spec_file

spec_file_path = os.getenv("SPEC_FILE_PATH")
app_spec_dict = load_and_parse_spec_file(spec_file_path) if spec_file_path else EXAMPLE_SPEC
client = SthaliCRUD(AppSpecification(**app_spec_dict))  # type: ignore
app = client.app
