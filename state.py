from typing import TypedDict, List, Annotated, Optional
from pydantic import BaseModel

class GraphState(BaseModel):
    conversation_history: List[str]
    last_prompt: str
    last_response: str
    last_response_to_user: str
    last_response_to_note: str
    
