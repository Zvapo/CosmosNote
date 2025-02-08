from langchain_community.tools.tavily_search import TavilySearchResults
import os
from dotenv import load_dotenv
from langchain_core.tools import tool
from langchain_core.tools import InjectedToolCallId
from typing import Annotated
from agents.models import SearchResult
from langchain_core.messages import ToolMessage
from langgraph.types import Command


# Load environment variables
load_dotenv()

# Get Tavily API key from environment
tavily_api_key = os.getenv("TAVILY_API_KEY")
if not tavily_api_key:
    raise ValueError("TAVILY_API_KEY environment variable is not set")

@tool
def web_search_tool(query: str):
    """ 
    Search the web for current information using Tavily API. 
    Search the web as a researcher would do.
    Ask follow up questions to get a better understanding of the query.

    Args:
        query (str): The search query to execute
        
    Returns:
        dict: Search results containing relevant information from the web
    """
    print('HELLO FROM WEB SEARCH TOOL')
    web_search_tool = TavilySearchResults(
        tavily_api_key=tavily_api_key,
        max_results=1,
        include_raw_content=True,
        include_images=False
    )

    return web_search_tool.invoke(query)