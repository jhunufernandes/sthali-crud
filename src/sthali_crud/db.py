from typing import Any

from fastapi import status

from .exceptions import SthaliCRUDException


class DB:
    """CRUD DB main class.

    Raises:
        DB.DBException: 'Not implemented'.
    """

    class DBException(SthaliCRUDException):
        def __init__(self) -> None:
            super().__init__("Not implemented", status.HTTP_501_NOT_IMPLEMENTED)

    async def create(self, *args, **kwargs) -> Any:
        raise DB.DBException()

    async def read(self, *args, **kwargs) -> Any:
        raise DB.DBException()

    async def update(self, *args, **kwargs) -> Any:
        raise DB.DBException()

    async def delete(self, *args, **kwargs) -> Any:
        raise DB.DBException()

    async def upsert(self, *args, **kwargs) -> Any:
        raise DB.DBException()

    async def read_all(self, *args, **kwargs) -> Any:
        raise DB.DBException()

    async def delete_all(self, *args, **kwargs) -> Any:
        raise DB.DBException()
