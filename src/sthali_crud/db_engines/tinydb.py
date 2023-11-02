from uuid import UUID

from fastapi import HTTPException, status
from tinydb import Query, TinyDB

from .base import BaseEngine


class TinyDBEngine(BaseEngine):
    db: TinyDB
    path: str
    table: str

    def __init__(self, path: str, table: str) -> None:
        self.db = TinyDB(path)
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

    async def db_insert_one(
        self, resource_id: UUID, resource_obj: dict, *args, **kwargs
    ) -> dict:
        self.db.table(self.table).insert(
            {"resource_id": str(resource_id), "resource_obj": resource_obj}
        )
        return {"id": str(resource_id), **resource_obj}

    async def db_select_one(self, resource_id: UUID, *args, **kwargs) -> dict:
        result = self._get(resource_id)
        return {"id": str(resource_id), **result["resource_obj"]}

    async def db_update_one(
        self, resource_id: UUID, resource_obj: dict, *args, **kwargs
    ) -> dict:
        self._get(resource_id)
        self.db.table(self.table).update(
            {"resource_obj": resource_obj}, Query().resource_id == str(resource_id)
        )
        return {"id": str(resource_id), **resource_obj}

    async def db_delete_one(self, resource_id: UUID, *args, **kwargs) -> None:
        self._get(resource_id)
        self.db.table(self.table).remove(Query().resource_id == str(resource_id))
        return

    async def db_select_all(self, *args, **kwargs) -> list[dict]:
        return [
            {"id": result["resource_id"], **result["resource_obj"]}
            for result in self.db.table(self.table).all()
        ]
