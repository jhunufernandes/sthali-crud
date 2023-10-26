from unittest.mock import patch
from fastapi import status
from fastapi.testclient import TestClient
from src.sthali_crud import DB, SthaliCRUD
from tests import (
    MockDB, RESOURCE_SPEC, PATH_WITH_ID, PATH_WITHOUT_ID, PAYLOAD_WITHOUT_ID, PAYLOAD_WITH_ID, RESPONSE_PATH)


class TestSthaliCRUD:
    _client = TestClient(SthaliCRUD(DB(), RESOURCE_SPEC).app)


class TestReturn501NotImplemented(TestSthaliCRUD):
    _json = {'detail': 'Not implemented'}
    _status_code = status.HTTP_501_NOT_IMPLEMENTED

    def test_create(self) -> None:
        _response = self._client.post(PATH_WITHOUT_ID, json=PAYLOAD_WITHOUT_ID)
        assert _response.status_code == self._status_code
        assert _response.json() == self._json

    def test_read(self) -> None:
        _response = self._client.get(PATH_WITH_ID)
        assert _response.status_code == self._status_code
        assert _response.json() == self._json

    def test_update_with_id_in_path_and_payload(self) -> None:
        _response = self._client.put(PATH_WITH_ID, json=PAYLOAD_WITH_ID)
        assert _response.status_code == self._status_code
        assert _response.json() == self._json

    def test_update_with_id_in_path(self) -> None:
        _response = self._client.put(PATH_WITH_ID, json=PAYLOAD_WITHOUT_ID)
        assert _response.status_code == self._status_code
        assert _response.json() == self._json

    def test_update_without_id_in_path(self) -> None:
        _response = self._client.put(PATH_WITHOUT_ID, json=PAYLOAD_WITH_ID)
        assert _response.status_code == self._status_code
        assert _response.json() == self._json

    def test_delete(self) -> None:
        _response = self._client.delete(PATH_WITH_ID)
        assert _response.status_code == self._status_code
        assert _response.json() == self._json


@patch('src.sthali_crud.db.DB.create', MockDB.create)
@patch('src.sthali_crud.db.DB.read', MockDB.read)
@patch('src.sthali_crud.db.DB.update', MockDB.update)
@patch('src.sthali_crud.db.DB.delete', MockDB.delete)
@patch('src.sthali_crud.db.DB.upsert', MockDB.upsert)
class TestReturn20XSuccesful(TestSthaliCRUD):
    _json = RESPONSE_PATH
    _status_code = status.HTTP_200_OK

    def test_create(self) -> None:
        _response = self._client.post(PATH_WITHOUT_ID, json=PAYLOAD_WITHOUT_ID)
        assert _response.status_code == status.HTTP_201_CREATED
        assert _response.json() == self._json

    def test_read(self) -> None:
        _response = self._client.get(PATH_WITH_ID)
        assert _response.status_code == self._status_code
        assert _response.json() == self._json

    def test_update_with_id_in_path_and_payload(self) -> None:
        _response = self._client.put(PATH_WITH_ID, json=PAYLOAD_WITH_ID)
        assert _response.status_code == self._status_code
        assert _response.json() == self._json

    def test_update_with_id_in_path(self) -> None:
        _response = self._client.put(PATH_WITH_ID, json=PAYLOAD_WITHOUT_ID)
        assert _response.status_code == self._status_code
        assert _response.json() == self._json

    def test_update_without_id_in_path(self) -> None:
        _response = self._client.put(PATH_WITHOUT_ID, json=PAYLOAD_WITH_ID)
        assert _response.status_code == self._status_code
        assert _response.json() == self._json

    def test_delete(self) -> None:
        _response = self._client.delete(PATH_WITH_ID)
        assert _response.status_code == status.HTTP_204_NO_CONTENT
        assert _response.text == ''
