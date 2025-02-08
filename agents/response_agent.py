from datetime import datetime
from agents.models import GraphState, ChatMessage
from langchain_openai import ChatOpenAI
from tools.web_search import web_search_tool
from typing import Literal
from langgraph.types import Command

async def response_agent(state: GraphState) -> Command[Literal["my_other_node"]]:
    """
    This agent is responsible for replying to user prompt.
    This agent can use web search to find current information.
    """
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
    tools = [web_search_tool] # add search tool
    llm.bind_tools(tools)
    
    user_message = state.user_prompt
    response = await llm.invoke(user_message)
    
    response_message = ChatMessage(
        role="assistant",
        content=str(response),
        timestamp=datetime.now().isoformat()
    )
    
    return Command(
        "my_other_node",
        {
            "conversation_history": [response_message],
            "user_prompt": state.user_prompt
        }
    )





