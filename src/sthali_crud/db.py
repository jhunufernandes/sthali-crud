from typing import Any
from fastapi import HTTPException


class DB:
    class DBException(HTTPException):
        detail: str
        status_code: int

        def __init__(self, detail: str, status_code: int = 400) -> None:
            self.detail = detail
            self.status_code = status_code
            super().__init__(status_code, detail)

    def read(self, *args, **kwargs) -> Any:
        raise NotImplementedError

    def update(self, *args, **kwargs) -> Any:
        raise NotImplementedError

    def upsert(self, *args, **kwargs) -> Any:
        raise NotImplementedError

    def delete(self, *args, **kwargs) -> Any:
        raise NotImplementedError
