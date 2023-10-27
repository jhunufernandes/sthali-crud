from typing import Any


class BaseEngine:
    async def db_insert_one(self, *args, **kwargs) -> Any:
        return Any

    async def db_select_one(self, *args, **kwargs) -> Any:
        return Any

    async def db_update_one(self, *args, **kwargs) -> Any:
        return Any

    async def db_delete_one(self, *args, **kwargs) -> Any:
        return Any

    async def db_select_all(self, *args, **kwargs) -> Any:
        return Any
