from typing import List, Annotated, Dict, Optional
from pydantic import BaseModel
import operator
from datetime import datetime
from langchain_core.messages import BaseMessage

class Note(BaseModel):
    title: str
    content: str
    tags: List[str]

class SearchResult(BaseModel):
    url: str
    content: str

# custom state graph inherits from the state graph class
class GraphState(BaseModel):
    user_prompt: str
    search_results: Annotated[List[SearchResult], operator.add] = []
    messages: Annotated[List[BaseMessage], operator.add] = []
    generated_note: Optional[Note] = None