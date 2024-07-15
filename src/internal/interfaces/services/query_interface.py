from abc import ABC, abstractmethod
from typing import Any, AsyncGenerator, Dict


class QueryInterface(ABC):
    @abstractmethod
    def query_db(self, query: str) -> AsyncGenerator[Dict[str, Any], None]:
        pass
