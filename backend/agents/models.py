from typing import List, Annotated, Dict, Optional
from pydantic import BaseModel
import operator
from datetime import datetime
from langchain_core.messages import BaseMessage


class Note(BaseModel):
    title: str
    content: str
    tags: List[str]


# custom state graph inherits from the state graph class
class GraphState(BaseModel):
    user_prompt: str
    search_results: Annotated[List[str], operator.add]
    messages: List[BaseMessage]
    generated_note: Optional[Note] = None
    research_results: Optional[List[str]] = None