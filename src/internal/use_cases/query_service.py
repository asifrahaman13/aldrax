from typing import Any, AsyncGenerator, Dict
from src.internal.interfaces.services.query_interface import QueryInterface
from src.constants.databases.available_databases import DatabaseKeys


class QueryService(QueryInterface):

    def __init__(self, query_database) -> None:
        self.query_database = query_database
        self.__db_keys = DatabaseKeys.get_keys()

    async def query_db(
        self, user: str, query: str, db: str
    ) -> AsyncGenerator[Dict[str, Any], None]:
        db_key = self.__db_keys.get(db)
        if not db_key:
            return

        available_client = {
            "_id": {"$oid": "6682efa74370bfd0532004ad"},
            "username": "exampleUsser",
            "sqlite": {
                "db_type": "sqlite",
                "projectName": "sqlite personal project",
                "username": "root",
                "description": "Working on a personal project to get insights on the data I have first to understand more on the project super query.",
                "connectionString": "sqlite:///company.db",
            },
        }
        if available_client and db_key in available_client:
            connection_string = available_client[db_key]
            async for response in self.query_database.query_database(
                query, **connection_string
            ):
                yield response
