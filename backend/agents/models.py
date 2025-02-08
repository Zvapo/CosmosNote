from typing import List, Annotated, Dict
from pydantic import BaseModel
import operator
from datetime import datetime
from langchain_core.messages import BaseMessage


class Note(BaseModel):
    title: str
    content: str
    tags: List[str]
    # follow_up_questions: List[str]


# custom state graph inherits from the state graph class
class GraphState(BaseModel):
    user_prompt: str
    search_results: Annotated[List[str], operator.add]
    messages: List[BaseMessage]
    note_titles: Annotated[List[str], operator.add]
