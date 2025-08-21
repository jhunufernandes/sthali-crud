"""{...}."""

import os

import uvicorn

from sthali_crud import AppSpecification, Config, SthaliCRUD

app_specification_file_path = os.getenv("APP_SPECIFICATION_FILE_PATH") or "volume/app_specification_sample.json"
config = Config(app_specification_file_path)
app_specification_dict = config.app_specification
client = SthaliCRUD(AppSpecification(**app_specification_dict))
app = client.app


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
