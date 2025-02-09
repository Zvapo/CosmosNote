from typing import List, Annotated, Dict, Optional
from pydantic import BaseModel
import operator
from datetime import datetime
from langchain_core.messages import BaseMessage
from typing_extensions import TypedDict

class Note(TypedDict):
    title: str
    content: str
    tags: List[str]

class SearchResult(TypedDict):
    source: str
    content: str

# custom state graph inherits from the state graph class
class GraphState(TypedDict):
    user_prompt: str
    messages: Annotated[List[BaseMessage], operator.add]
    generated_note: Optional[Note] = None
