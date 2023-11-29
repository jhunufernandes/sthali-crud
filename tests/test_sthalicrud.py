from unittest.mock import patch

from fastapi import status
from fastapi.testclient import TestClient

from src.sthali_crud import SthaliCRUD
from tests import (
    APP_SPEC,
    PATH_WITH_ID,
    PATH_WITHOUT_ID,
    PAYLOAD_WITH_ID_STR,
    PAYLOAD_WITHOUT_ID,
    MockDB,
)


class TestSthaliCRUD:
    client = TestClient(SthaliCRUD(APP_SPEC).app)


@patch("src.sthali_crud.db.DB.create", MockDB.create)
@patch("src.sthali_crud.db.DB.read", MockDB.read)
@patch("src.sthali_crud.db.DB.update", MockDB.update)
@patch("src.sthali_crud.db.DB.delete", MockDB.delete)
class TestReturn20XSuccesful(TestSthaliCRUD):
    json = PAYLOAD_WITH_ID_STR
    status_code = status.HTTP_200_OK

    def test_create(self) -> None:
        response = self.client.post(PATH_WITHOUT_ID, json=PAYLOAD_WITHOUT_ID)
        assert response.status_code == status.HTTP_201_CREATED
        assert response.json() == self.json

    def test_read(self) -> None:
        response = self.client.get(PATH_WITH_ID)
        assert response.status_code == self.status_code
        assert response.json() == self.json

    def test_update_with_id_in_path_and_payload(self) -> None:
        response = self.client.put(PATH_WITH_ID, json=PAYLOAD_WITH_ID_STR)
        assert response.status_code == self.status_code
        assert response.json() == self.json

    def test_update_with_id_in_path(self) -> None:
        response = self.client.put(PATH_WITH_ID, json=PAYLOAD_WITHOUT_ID)
        assert response.status_code == self.status_code
        assert response.json() == self.json

    def test_update_without_id_in_path(self) -> None:
        response = self.client.put(PATH_WITHOUT_ID, json=PAYLOAD_WITH_ID_STR)
        assert response.status_code == self.status_code
        assert response.json() == self.json

    def test_delete(self) -> None:
        response = self.client.delete(PATH_WITH_ID)
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert response.text == ""
