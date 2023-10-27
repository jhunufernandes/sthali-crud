from os import getenv, path

from src.sthali_crud import AppSpecification, SthaliCRUD

TINYDB_PATH = path.join(path.dirname(__file__), "tinydb.json")
SPEC = {
    "resources": [
        {
            "db": {"engine": "tinydb", "path": TINYDB_PATH},
            "name": "samples",
            "fields": [
                {
                    "name": "str",
                    "type": str,
                },
                {
                    "name": "str or none",
                    "type": str,
                },
            ],
        },
        {
            "db": {"engine": "tinydb", "path": TINYDB_PATH},
            "name": "dogs",
            "fields": [
                {
                    "name": "name",
                    "type": str,
                },
                {
                    "name": "fur",
                    "type": bool,
                },
            ],
        },
    ]
}

sthalicrud = SthaliCRUD(AppSpecification(**SPEC))
app = sthalicrud.app
