"""Methods for CRUD.
"""
from pydantic import BaseModel
from .db import DB
from .models import Models, CreateInputModel


class CRUD:
    _db: DB
    _models: Models

    def __init__(self, db: DB, models: Models) -> None:
        self._db = db
        self._models = models

    @classmethod
    def replace_model(cls, model: type[BaseModel]) -> None:
        cls._model = model

    # def create(self, resource: type[BaseModel]) -> type[BaseModel]:
    def create(self, resource: CreateInputModel):
        breakpoint()
        return resource
