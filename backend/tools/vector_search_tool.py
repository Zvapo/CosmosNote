from langchain_core.tools import tool
from langgraph.types import Command
from typing import Annotated
from langchain_core.tools.base import InjectedToolCallId
from langchain_core.messages import ToolMessage
from agents.models import GraphState
@tool
def vector_search_tool(state: GraphState, tool_call_id: Annotated[str, InjectedToolCallId]):
    """
    Search the vector database with research papers about expoplanets.
    
    Args:
        query (str): The search query to execute
    """
    search_results = "LATEST RESEARCH SAYS THAT THE BEST EXPOPLANET TO LIVE ON IS MESSI-0101010!!!"
    return Command(
        update={
            "search_results": [search_results],
            # update the message history
            "messages": [ToolMessage("Successfully looked up user information", tool_call_id=tool_call_id)]
        }
    )