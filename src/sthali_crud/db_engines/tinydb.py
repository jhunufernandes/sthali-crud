from os import path
from uuid import UUID

from fastapi import HTTPException, status
from tinydb import Query, TinyDB

from src.sthali_crud.db_engines.base import BaseEngine

TINYDB_PATH = path.join(path.dirname(__file__), "../../../tinydb.json")


class TinyDBEngine(BaseEngine):
    db = TinyDB(TINYDB_PATH)
    table: str

    def __init__(self, table) -> None:
        self.table = table

    def _get(self, resource_id: UUID, raise_exception: bool = True) -> dict:
        try:
            result = self.db.table(self.table).search(
                Query().resource_id == str(resource_id)
            )
            assert result and raise_exception, "not found"
        except AssertionError as exception:
            raise HTTPException(
                status.HTTP_404_NOT_FOUND, exception.args[0]
            ) from exception
        else:
            return result[0]

    async def db_insert_one(self, resource_id: UUID, resource_obj: dict) -> dict:
        self.db.table(self.table).insert(
            {"resource_id": str(resource_id), "resource_obj": resource_obj}
        )
        return {"id": str(resource_id), **resource_obj}

    async def db_select_one(self, resource_id: UUID, *args, **kwargs) -> dict:
        result = self._get(resource_id)
        return {"id": str(resource_id), **result["resource_obj"]}

    async def db_update_one(self, resource_id: UUID, resource_obj: dict) -> dict:
        self._get(resource_id)
        self.db.table(self.table).update(
            {"resource_obj": resource_obj}, Query().resource_id == str(resource_id)
        )
        return {"id": str(resource_id), **resource_obj}

    async def db_delete_one(self, resource_id: UUID) -> None:
        self._get(resource_id)
        self.db.table(self.table).remove(Query().resource_id == str(resource_id))
        return
