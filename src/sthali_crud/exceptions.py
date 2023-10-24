from fastapi import HTTPException, status
from pydantic_core import ErrorDetails


class SthaliCRUDException(HTTPException):
    """SthaliCRUD Exception.

    Args:
        HTTPException (Exception): FastAPI Model Exception.
    """

    detail: str | list[ErrorDetails]
    status_code: int

    def __init__(
        self,
        detail: str | list[ErrorDetails],
        status_code: int = status.HTTP_400_BAD_REQUEST,
    ) -> None:
        self.detail = detail
        self.status_code = status_code
        super().__init__(status_code, detail)
