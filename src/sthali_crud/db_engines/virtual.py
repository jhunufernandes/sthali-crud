from uuid import UUID

from fastapi import HTTPException, status

from .base import BaseEngine


class VirtualEngine(BaseEngine):
    db = {}

    def __init__(self, _: str, table: str) -> None:
        self.table = table

    def _get(self, resource_id: UUID) -> dict:
        try:
            return self.db[resource_id]
        except KeyError as exception:
            raise HTTPException(status.HTTP_404_NOT_FOUND, "not found") from exception

    async def db_insert_one(self, resource_id: UUID, resource_obj: dict) -> dict:
        self.db[resource_id] = resource_obj
        return {"id": resource_id, **resource_obj}

    async def db_select_one(self, resource_id: UUID) -> dict:
        return {"id": resource_id, **self._get(resource_id)}

    async def db_update_one(self, resource_id: UUID, resource_obj: dict) -> dict:
        self._get(resource_id)
        self.db[resource_id] = resource_obj
        return {"id": resource_id, **resource_obj}

    async def db_delete_one(self, resource_id: UUID) -> None:
        self._get(resource_id)
        self.db.pop(resource_id)
        return None

    async def db_select_all(self) -> list[dict]:
        return [{"id": k, **v} for k, v in self.db.items()]
