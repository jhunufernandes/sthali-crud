from unittest import IsolatedAsyncioTestCase
from src.sthali_crud.db import DB


class TestDB(IsolatedAsyncioTestCase):
    def setUp(self):
        self._db = DB()

    async def test_create(self) -> None:
        with self.assertRaises(DB.DBException):
            await self._db.create()

    async def test_read(self) -> None:
        with self.assertRaises(DB.DBException):
            await self._db.read()

    async def test_update(self) -> None:
        with self.assertRaises(DB.DBException):
            await self._db.update()

    async def test_delete(self) -> None:
        with self.assertRaises(DB.DBException):
            await self._db.delete()

    async def test_upsert(self) -> None:
        with self.assertRaises(DB.DBException):
            await self._db.upsert()

    async def test_read_all(self) -> None:
        with self.assertRaises(DB.DBException):
            await self._db.read_all()

    async def test_delete_all(self) -> None:
        with self.assertRaises(DB.DBException):
            await self._db.delete_all()
