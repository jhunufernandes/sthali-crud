from uuid import UUID

from .db_engines import DBEngine
from .types import DBSpecification


class DB(DBEngine):
    def __init__(self, db_spec: DBSpecification, table: str) -> None:
        super().__init__(db_spec, table)

    async def create(self, resource_id: UUID, resource_obj: dict, *args, **kwargs) -> dict:
        return await self.db_insert_one(resource_id=resource_id, resource_obj=resource_obj)

    async def read(self, resource_id: UUID, *args, **kwargs) -> dict:
        return await self.db_select_one(resource_id=resource_id)

    async def update(self, resource_id: UUID, resource_obj: dict, *args, **kwargs) -> dict:
        return await self.db_update_one(resource_id=resource_id, resource_obj=resource_obj)

    async def delete(self, resource_id: UUID, *args, **kwargs) -> None:
        return await self.db_delete_one(resource_id=resource_id)

    async def read_all(self, *args, **kwargs) -> dict:
        return await self.db_select_all()
