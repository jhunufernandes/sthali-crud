class BaseEngine:
    async def db_insert_one(self) -> NotImplementedError:
        raise NotImplementedError

    async def db_select_one(self) -> NotImplementedError:
        raise NotImplementedError

    async def db_update_one(self) -> NotImplementedError:
        raise NotImplementedError

    async def db_delete_one(self) -> NotImplementedError:
        raise NotImplementedError

    async def db_select_all(self) -> NotImplementedError:
        raise NotImplementedError
