"""{...}."""

from os import getenv

from dotenv import load_dotenv

load_dotenv()


class Config:
    """{...}."""

    def __init__(self) -> None:
        """{...}."""
        database_uri = getenv("DATABASE_URI")

        if not isinstance(database_uri, str):
            msg = "DATABASE_URI environment variable is not set"
            raise TypeError(msg)

        self.database_uri = database_uri

    # def get_api_router_permissions(self, router_name: str) -> bool:
    #     return bool(getenv(f"API_{router_name.upper()}"))

    # def get_views_router_permissions(self, router_name: str) -> bool:
    #     return bool(getenv(f"API_{router_name.upper()}"))


config = Config()
