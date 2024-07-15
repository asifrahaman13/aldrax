from src.infastructure.repositories.sqlite_query_repository import SqliteQueryRepository
from src.internal.use_cases.query_service import QueryService
from src.ConnectionManager.ConnectionManager import ConnectionManager
from src.infastructure.repositories.helper.handle_answer_types import HandleAnswerTypes
from config.config import REDIS_HOST, REDIS_PORT, REDIS_PASSWORD



class DIContainer:
    def __init__(self):
        self.__instances = {}

    def get_sqlite_query_repository(self):
        if "sqlite_query_repository" not in self.__instances:
            self.__instances["sqlite_query_repository"] = SqliteQueryRepository(
                HandleAnswerTypes()
            )
        return self.__instances["sqlite_query_repository"]

    def get_sqlite_query_database_service(self):
        if "sqlite_query_service" not in self.__instances:
            self.__instances["sqlite_query_service"] = QueryService(
                self.get_sqlite_query_repository() 
            )
        return self.__instances["sqlite_query_service"]


container = DIContainer()
websocket_manager = ConnectionManager(REDIS_HOST, REDIS_PORT, REDIS_PASSWORD)


def get_sqlite_query_database_service():
    return container.get_sqlite_query_database_service()
