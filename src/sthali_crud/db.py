from uuid import UUID

from src.sthali_crud.db_engines import AVAILABLE_ENGINES, DBEngine
from src.sthali_crud.db_engines.base import BaseEngine


class DB(DBEngine):
    engine: type[BaseEngine]
    table: str

    def __init__(self, engine: AVAILABLE_ENGINES, table: str) -> None:
        super().__init__(engine, table)

    async def create(self, resource_id: UUID, resource_obj: dict, *args, **kwargs) -> dict:
        return await self.db_insert_one(resource_id=resource_id, resource_obj=resource_obj)

    async def read(self, resource_id: UUID, *args, **kwargs) -> dict:
        return await self.db_select_one(resource_id=resource_id)

    async def update(self, resource_id: UUID, resource_obj: dict, *args, **kwargs) -> dict:
        return await self.db_update_one(resource_id=resource_id, resource_obj=resource_obj)

    async def delete(self, resource_id: UUID, *args, **kwargs) -> None:
        return await self.db_delete_one(resource_id=resource_id)
