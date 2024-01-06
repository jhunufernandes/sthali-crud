from unittest.mock import AsyncMock
from uuid import uuid4

from src.sthali_crud import crud, db, models, types

# APP CONSTANTS
DB_SPEC = types.DBSpecification(
    engine="Default",
    path="",
)
FIELD_DEF = types.FieldDefinition(
    name="field_1",
    type=str,
)
RESOURCE_SPEC = types.ResourceSpecification(
    db=DB_SPEC,
    name="test_resource",
    fields=[FIELD_DEF],
)
APP_SPEC = types.AppSpecification(resources=[RESOURCE_SPEC])


# ROUTES CONSTANTS
PATH_WITHOUT_ID = f"/{RESOURCE_SPEC.name}/"
ID = uuid4()
PATH_WITH_ID = f"{PATH_WITHOUT_ID}{ID}/"
PAYLOAD_WITHOUT_ID = {FIELD_DEF.name: "value_1"}
PAYLOAD_WITH_ID = {"id": ID, **PAYLOAD_WITHOUT_ID}
PAYLOAD_WITH_ID_STR = {"id": str(ID), **PAYLOAD_WITHOUT_ID}


# MOCKS CONSTANTS
CREATE = AsyncMock(return_value=PAYLOAD_WITH_ID)
READ = AsyncMock(return_value=PAYLOAD_WITH_ID)
UPDATE = AsyncMock(return_value=PAYLOAD_WITH_ID)
UPSERT = AsyncMock(return_value=PAYLOAD_WITH_ID)
DELETE = AsyncMock(return_value=None)
READ_ALL = AsyncMock(return_value=[PAYLOAD_WITH_ID])


class MockCRUD(crud.CRUD):
    create = CREATE
    read = READ
    update = UPDATE
    upsert = UPSERT
    delete = DELETE
    read_all = READ_ALL


class MockDB(db.DB):
    create = CREATE
    read = READ
    update = UPDATE
    delete = DELETE
    read_all = READ_ALL


class MockModels(models.Models):
    create_model = models.BaseModel
    response_model = models.BaseModel
    update_model = models.BaseModel
    upsert_model = models.BaseModel
