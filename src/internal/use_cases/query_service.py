import asyncio
import json
from typing import Any, AsyncGenerator, Dict
from src.internal.entities.router_models import QueryResponse
from src.internal.interfaces.services.query_interface import QueryInterface


class QueryService(QueryInterface):

    def __init__(self, sqlite_repository, redis_repository, openai_repository) -> None:
        self.sqlite_repository = sqlite_repository
        self.redis_repository = redis_repository
        self.openai_repository = openai_repository

    async def query_db(self, query: str) -> AsyncGenerator[Dict[str, Any], None]:

        await asyncio.sleep(0)
        yield QueryResponse(message="Querying the database", status=True)
        await asyncio.sleep(0)

        # Check if the query is in the cache
        cache_key = self.redis_repository.get_cached_key(query)
        cached_result = self.redis_repository.get_cached_data(cache_key)

        if cached_result:
            results = json.loads(cached_result.decode("utf-8"))
            headers = json.loads(
                self.redis_repository.get_cached_data(f"{cache_key}_headers").decode(
                    "utf-8"
                )
            )
        else:
            await asyncio.sleep(0)
            yield QueryResponse(message="Thinking", status=True)
            await asyncio.sleep(0)
            # Get the SQL query from OpenAI
            query_result = self.openai_repository.get_llm_response(query)

            await asyncio.sleep(0)
            yield QueryResponse(message="Executing the query", status=True)
            await asyncio.sleep(0)
            results, headers = self.sqlite_repository.query_database(
                query_result, "databases/company.db"
            )

            # Store result in cache with expiration of 5 minutes
            self.redis_repository.set_cache_data(cache_key, json.dumps(results))
            self.redis_repository.set_cache_data(
                f"{cache_key}_headers", json.dumps(headers)
            )

        if results:
            await asyncio.sleep(0)
            yield QueryResponse(json_message=results, message=results, status=False)
            await asyncio.sleep(0)
        else:
            print("No results found.")
