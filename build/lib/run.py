from os import getenv

from spec_example import EXAMPLE_SPEC
from sthali_crud import AppSpecification, SthaliCRUD, load_and_parse_spec_file

spec_file_path = getenv("SPEC_FILE_PATH")
spec_dict = load_and_parse_spec_file(spec_file_path) if spec_file_path else EXAMPLE_SPEC
client = SthaliCRUD(AppSpecification(**spec_dict))
app = client.app
