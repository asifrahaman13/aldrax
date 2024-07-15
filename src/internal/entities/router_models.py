from typing import Annotated, Any, Dict, Optional
from pydantic import BaseModel, Field


class QueryResponse(BaseModel):
    json_message: Any = Field(None, description="The json message")
    message: Annotated[str, "The response message"] = None
    status: Annotated[Optional[bool], "The status of the response"]
    sql_query: Annotated[Optional[str], "The SQL query"] = None
    answer_type: Annotated[Optional[str], "The type of the answer"] = None
