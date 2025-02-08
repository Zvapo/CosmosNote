from langchain_core.tools import tool
from langgraph.types import Command
from typing import Annotated
from langchain_core.tools.base import InjectedToolCallId
from langchain_core.messages import ToolMessage
from agents.models import SearchResult, GraphState

@tool
def vector_search_tool(query: str):
    """
    This tools job is to search the vector database with research papers about exoplanets.
    Search the vector database as a researcher would do.
    Search the vector database for key words and phrases related to the query.

    Args:
        query (str): The search query to execute
    """
    print('HELLO FROM VECTOR SEARCH TOOL')
    content = "LATEST RESEARCH SAYS THAT THE BEST EXPOPLANET TO LIVE ON IS MESSI-0101010!!!"

    return content
