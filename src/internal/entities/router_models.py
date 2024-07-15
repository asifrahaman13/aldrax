from typing import Annotated, Any, Dict, Optional
from pydantic import BaseModel, Field


class QueryResponse(BaseModel):
    json_message: Any = Field(None, description="The json message")
    message: Annotated[str, "The response message"] = None
    status: Annotated[Optional[bool], "The status of the response"]
    answer_type: Annotated[Optional[str], "The type of the answer"] = None
