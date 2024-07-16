from openai import OpenAI
import redis
from src.infastructure.repositories.vector_db_repository import EmbeddingService, QdrantQueryRepository, QdrantService
from src.infastructure.repositories.openai_repository import OpenAIRepository
from src.infastructure.repositories.redis_repository import RedisRepository
from src.infastructure.repositories.sqlite_query_repository import SqliteQueryRepository
from src.internal.use_cases.query_service import QueryService
from src.ConnectionManager.ConnectionManager import ConnectionManager
from config.config import REDIS_HOST, REDIS_PORT, OPENAI_API_KEY, REDIS_PORT, REDIS_HOST, QDRANT_API_ENDPOINT, QDRANT_API_KEY


class DIContainer:
    def __init__(self):
        self.__instances = {}

    def get_redis_repository(self):
        if "redis_repository" not in self.__instances:
            redis_client = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=0)
            self.__instances["redis_repository"] = RedisRepository(redis_client)
        return self.__instances["redis_repository"]
    
    def get_openai_repository(self):
        if "openai_repository" not in self.__instances:
            openai_client = OpenAI(api_key=OPENAI_API_KEY)
            self.__instances["openai_repository"] = OpenAIRepository(openai_client)
        return self.__instances["openai_repository"]

    def get_sqlite_query_repository(self):
        if "sqlite_query_repository" not in self.__instances:
            self.__instances["sqlite_query_repository"] = SqliteQueryRepository()
        return self.__instances["sqlite_query_repository"]

    def get_vector_db_repository(self):
        if "vectordb_repoitory" not in self.__instances:
            embedding_service=EmbeddingService()
            qdrant_service=QdrantService(url=QDRANT_API_ENDPOINT, api_key=QDRANT_API_KEY)
            self.__instances["vectordb_repoitory"]= QdrantQueryRepository(embedding_service, qdrant_service)
        return self.__instances["vectordb_repoitory"]

    def get_sqlite_query_database_service(self):
        if "sqlite_query_service" not in self.__instances:
            self.__instances["sqlite_query_service"] = QueryService(
                self.get_sqlite_query_repository(),
                self.get_redis_repository(),
                self.get_openai_repository(),
                self.get_vector_db_repository()
            )
        return self.__instances["sqlite_query_service"]


container = DIContainer()
websocket_manager = ConnectionManager(REDIS_HOST, REDIS_PORT)


def get_sqlite_query_database_service():
    return container.get_sqlite_query_database_service()
