from typing import Any, Literal

from sthali_crud.db_engines.base import BaseEngine
from sthali_crud.db_engines.postgres import PostgresEngine
from sthali_crud.db_engines.tinydb import TinyDBEngine

AVAILABLE_ENGINES = Literal["postgres", "tinydb"]


class Engine:
    postgres = PostgresEngine
    tinydb = TinyDBEngine


class DBEngine:
    engine: type[BaseEngine]

    def __init__(self, engine: AVAILABLE_ENGINES, table: str) -> None:
        db_engine = getattr(Engine, engine)
        self.engine = db_engine(table)

    async def db_insert_one(self, *args, **kwargs) -> Any:
        return await self.engine.db_insert_one(*args, **kwargs)

    async def db_select_one(self, *args, **kwargs) -> Any:
        return await self.engine.db_select_one(*args, **kwargs)

    async def db_update_one(self, *args, **kwargs) -> Any:
        return await self.engine.db_update_one(*args, **kwargs)

    async def db_delete_one(self, *args, **kwargs) -> Any:
        return await self.engine.db_delete_one(*args, **kwargs)
