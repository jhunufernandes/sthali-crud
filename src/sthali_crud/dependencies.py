"""Pagination dependency for CRUD API endpoints."""

from typing import Annotated

from fastapi import Depends
from pydantic import BaseModel, Field, NonNegativeInt


class PaginateParameters(BaseModel):
    """Query parameters for paginating list results.

    Attributes:
        skip: The number of items to skip. Defaults to 0.
        limit: The maximum number of items to return. Defaults to 100.
    """

    skip: Annotated[
        NonNegativeInt,
        Field(default=0, description="The number of items to skip"),
    ]
    limit: Annotated[
        NonNegativeInt,
        Field(default=100, description="The maximum number of items to return"),
    ]


paginate_parameters = Annotated[PaginateParameters | None, Depends(PaginateParameters)]
