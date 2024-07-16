import asyncio
import json
from typing import Any, AsyncGenerator, Dict
from src.internal.entities.router_models import QueryResponse
from src.internal.interfaces.services.query_interface import QueryInterface


class QueryService(QueryInterface):

    def __init__(
        self,
        sqlite_repository,
        redis_repository,
        openai_repository,
        vector_db_repository,
    ) -> None:
        self.sqlite_repository = sqlite_repository
        self.redis_repository = redis_repository
        self.openai_repository = openai_repository
        self.vector_db_repository = vector_db_repository

    async def query_db(self, query: str) -> AsyncGenerator[Dict[str, Any], None]:

        await asyncio.sleep(0)
        yield QueryResponse(
            message="Querying the database", answer_type="status", status=True
        )
        await asyncio.sleep(0)

        # Check if the query is in the cache
        cache_key = self.redis_repository.get_cached_key(query)
        cached_result = self.redis_repository.get_cached_data(cache_key)
        cached_sql_query = self.redis_repository.get_cached_data(f"{cache_key}_sql")

        sql_query = None

        if cached_result and cached_sql_query:
            results = json.loads(cached_result.decode("utf-8"))
            headers = json.loads(
                self.redis_repository.get_cached_data(f"{cache_key}_headers").decode(
                    "utf-8"
                )
            )
            sql_query = cached_sql_query.decode("utf-8")
            await asyncio.sleep(0)
            yield QueryResponse(
                sql_query=sql_query, answer_type="sql_query", status=False
            )
            await asyncio.sleep(0)
        else:
            await asyncio.sleep(0)
            yield QueryResponse(message="Thinking", answer_type="status", status=True)
            await asyncio.sleep(0)
            # Get top 5 result from the vector database and then pass it to the llm for context.
            top_suggestions = self.vector_db_repository.query_text(query, "1")

            print("######################### top result", top_suggestions)
            query_result = self.openai_repository.get_llm_response(
                query, top_suggestions
            )
            sql_query = query_result

            await asyncio.sleep(0)
            yield QueryResponse(
                message="Executing the query", answer_type="status", status=True
            )
            await asyncio.sleep(0)

            # Get the SQL query from OpenAI

            results, headers = self.sqlite_repository.query_database(
                query_result, "databases/company.db"
            )

            # Store SQL query and result in cache with expiration of 5 minutes
            self.redis_repository.set_cache_data(f"{cache_key}_sql", query_result)
            self.redis_repository.set_cache_data(cache_key, json.dumps(results))
            self.redis_repository.set_cache_data(
                f"{cache_key}_headers", json.dumps(headers)
            )

        if results:
            await asyncio.sleep(0)
            yield QueryResponse(
                json_message=results,
                message=results,
                answer_type="table_response",
                status=False,
            )
            await asyncio.sleep(0)

            await asyncio.sleep(0)
            yield QueryResponse(
                sql_query=sql_query, answer_type="sql_query", status=False
            )
            await asyncio.sleep(0)
        else:
            print("No results found.")
