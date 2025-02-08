from typing import TypedDict, List, Annotated, Optional
from pydantic import BaseModel
import operator
from datetime import datetime

class ChatMessage(BaseModel):
    role: str # either user or agent
    content: str # message content
    timestamp: str = str(datetime.now().isoformat()) 

class GraphState(BaseModel):
    conversation_history: Annotated[List[ChatMessage], operator.add]
    user_prompt: str
    generated_note: str

class Agent0Response(BaseModel):
    response: str
    
