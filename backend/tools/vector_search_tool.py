from langchain_core.tools import tool
from langgraph.types import Command
from typing import Annotated
from langchain_core.tools.base import InjectedToolCallId
from langchain_core.messages import ToolMessage
from agents.models import SearchResult, GraphState

@tool
def vector_search_tool(query: str, state: GraphState, tool_call_id: Annotated[str, InjectedToolCallId]):
    """
    Search the vector database with research papers about expoplanets.
    
    Args:
        query (str): The search query to execute
    """
    print('HELLO FROM VECTOR SEARCH TOOL')
    content = "LATEST RESEARCH SAYS THAT THE BEST EXPOPLANET TO LIVE ON IS MESSI-0101010!!!"
    search_result = SearchResult(
        source='Vector Database',
        content=content
    )

    return Command(
        update={
            "messages": [ToolMessage(
                content=search_result.content,
                tool_call_id=tool_call_id
            )],
            "search_results": [search_result]
        }
    )
