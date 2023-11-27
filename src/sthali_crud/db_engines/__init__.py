from typing import Any

from ..types import DBSpecification
from ..db_engines.base import BaseEngine
from ..db_engines.postgres import PostgresEngine
from ..db_engines.tinydb import TinyDBEngine


class Engine:
    postgres = PostgresEngine
    tinydb = TinyDBEngine


class DBEngine:
    engine: type[BaseEngine]

    def __init__(self, db_spec: DBSpecification, table: str) -> None:
        db_engine = getattr(Engine, db_spec.engine)
        self.engine = db_engine(db_spec.path, table)

    async def db_insert_one(self, *args, **kwargs) -> Any:
        return await self.engine.db_insert_one(*args, **kwargs)

    async def db_select_one(self, *args, **kwargs) -> Any:
        return await self.engine.db_select_one(*args, **kwargs)

    async def db_update_one(self, *args, **kwargs) -> Any:
        return await self.engine.db_update_one(*args, **kwargs)

    async def db_delete_one(self, *args, **kwargs) -> Any:
        return await self.engine.db_delete_one(*args, **kwargs)

    async def db_select_all(self, *args, **kwargs) -> Any:
        return await self.engine.db_select_all(*args, **kwargs)
