from unittest.mock import Mock

from src.sthali_crud.db_engines import (
    base,
    DBEngine,
    tinydb,
)


from tests import CREATE, DELETE, READ, READ_ALL, UPDATE


class MockDBEngine(DBEngine):
    db_insert_one = CREATE
    db_select_one = READ
    db_update_one = UPDATE
    db_delete_one = DELETE
    db_select_all = READ_ALL


class MockEngine(base.BaseEngine):
    db_insert_one = CREATE
    db_select_one = READ
    db_update_one = UPDATE
    db_delete_one = DELETE
    db_select_all = READ_ALL


class MockTinyDB(tinydb.TinyDB):
    table = Mock()
