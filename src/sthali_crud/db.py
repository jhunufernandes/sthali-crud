"""Methods for DB.
"""
from typing import Any
from fastapi import HTTPException


class DB:
    """DB main class.
    """
    class DBException(HTTPException):
        """DB Exception.

        Args:
            HTTPException (Exception): FastAPI base Exception.
        """
        def __init__(self, detail: str, status_code: int = 400) -> None:
            self.detail = detail
            self.status_code = status_code
            super().__init__(status_code, detail)

    def create(self, *args, **kwargs) -> Any:
        raise self.DBException('Method not defined.')

    def read(self, *args, **kwargs) -> Any:
        raise self.DBException('Method not defined.')

    def update(self, *args, **kwargs) -> Any:
        raise self.DBException('Method not defined.')

    def delete(self, *args, **kwargs) -> Any:
        raise self.DBException('Method not defined.')
