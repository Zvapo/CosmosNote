from langchain_community.tools.tavily_search import TavilySearchResults
import os
from dotenv import load_dotenv
from langchain_core.tools import tool
from langchain_core.runnables import RunnableConfig
from langchain_core.tools import InjectedToolCallId
from typing import Annotated
from agents.models import GraphState, SearchResult
from langchain_core.messages import ToolMessage
from langgraph.types import Command


# Load environment variables
load_dotenv()

# Get Tavily API key from environment
tavily_api_key = os.getenv("TAVILY_API_KEY")
if not tavily_api_key:
    raise ValueError("TAVILY_API_KEY environment variable is not set")

@tool
def web_search_tool(query: str, tool_call_id: Annotated[str, InjectedToolCallId]):
    """ 
    Search the web for current information using Tavily API.
    
    Args:
        query (str): The search query to execute
        
    Returns:
        dict: Search results containing relevant information from the web
    """
    web_search_tool = TavilySearchResults(
        tavily_api_key=tavily_api_key,
        max_results=1,
        include_raw_content=True,
        include_images=False
    )

    print('===============================================  ')
    print('passed to the tool', query)
    results = web_search_tool.invoke(query)
    print('response from tavily:', results)
    print('===============================================  ')

    # Handle the first result
    if results and len(results) > 0:
        result = results[0]  # Get first result
        search_result = SearchResult(
            url=result.get('url', ''),
            content=result.get('content', '')
        )
        return Command(
            update={
                "search_results": [search_result],
                "messages": [ToolMessage(
                    content=f"Found information: {search_result.content}", 
                    tool_call_id=tool_call_id
                )]
            }
        )
    else:
        return Command(
            update={
                "messages": [ToolMessage(
                    content="No results found", 
                    tool_call_id=tool_call_id
                )]
            }
        )