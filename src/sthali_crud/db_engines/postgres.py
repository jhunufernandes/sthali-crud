from .base import BaseEngine


class PostgresEngine(BaseEngine):
    def __init__(self, path: str, table: str) -> None:
        # self.db = TinyDB(path)
        self.table = table
