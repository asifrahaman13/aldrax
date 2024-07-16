from abc import ABC, abstractmethod
from typing import List
from typing import Any, AsyncGenerator, Dict


class QueryInterface(ABC):
    @abstractmethod
    def query_db(self, query: str) -> AsyncGenerator[Dict[str, Any], None]:
        pass

    @abstractmethod
    def add_data_to_vector_db(
        self, user_query: str, sql_query: str, source: List[Dict[str, Any]]
    ) -> bool:
        pass
