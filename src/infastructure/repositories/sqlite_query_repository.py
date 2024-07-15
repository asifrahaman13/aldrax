import asyncio
from src.internal.entities.router_models import QueryResponse
from sqlmodel import SQLModel, Session, create_engine
from sqlalchemy import text


class SqliteQueryRepository:
    def __init__(self, handle_answer_type) -> None:
        self.handle_answer_type = handle_answer_type

    async def query_database(self, user_query: str, *args, **kwargs):
        pass
