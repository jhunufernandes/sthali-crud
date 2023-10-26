from unittest.mock import AsyncMock
from src.sthali_crud import CRUD, DB, FieldDefinition, Models, ResourceSpecification


ID = '823551e3-4dcc-4abb-878c-1809a0a38db6'
PAYLOAD_WITHOUT_ID = {
    'name': 'jhunu',
    'age': 27
}
PAYLOAD_WITH_ID = {
    'id': ID,
    **PAYLOAD_WITHOUT_ID
}
RESPONSE_PATH = PAYLOAD_WITH_ID
RESOURCE_SPEC = ResourceSpecification(
    name='people',
    fields=[
        FieldDefinition(
            name='name',
            type=str,
        ),
        FieldDefinition(
            name='age',
            type=int,
        ),
    ]
)
PATH_WITH_ID = f"/{RESOURCE_SPEC.name}/{ID}/"
PATH_WITHOUT_ID = f"/{RESOURCE_SPEC.name}/"


class MockCRUD(CRUD):
    create = AsyncMock(return_value=RESPONSE_PATH)
    read = AsyncMock(return_value=RESPONSE_PATH)
    update = AsyncMock(return_value=RESPONSE_PATH)
    update = AsyncMock(return_value=RESPONSE_PATH)
    delete = AsyncMock(return_value=None)


class MockDB(DB):
    create = AsyncMock(return_value=RESPONSE_PATH)
    read = AsyncMock(return_value=RESPONSE_PATH)
    update = AsyncMock(return_value=RESPONSE_PATH)
    delete = AsyncMock(return_value=None)
    upsert = AsyncMock(return_value=RESPONSE_PATH)


class MockModels(Models):
    create_model = AsyncMock(return_value={})
    response_model = AsyncMock(return_value={})
    update_model = AsyncMock(return_value={})
    update_model = AsyncMock(return_value={})
