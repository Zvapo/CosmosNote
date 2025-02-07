from typing import Dict, Any
from tavily_api import TavilyClient
from langchain_core.tools import Tool
from dotenv import load_dotenv
import os

load_dotenv()

tavily = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))

def web_search(query: str) -> Dict[str, Any]:
    """
    Search the web using Tavily's API.
    
    Args:
        query (str): The search query to execute
        
    Returns:
        Dict[str, Any]: Search results containing text and metadata
    """
    try:
        search_result = tavily.search(
            query=query,
            search_depth="advanced",
            include_raw_content=True,
            include_images=False
        )
        return {
            "results": search_result,
            "status": "success"
        }
    except Exception as e:
        return {
            "results": None,
            "status": "error",
            "error": str(e)
        }

TAVILY_TOOL_DESCRIPTION = """
    Searches the web for current information on a given query.
    Use this tool when you need to find up-to-date information or verify facts.
"""

tavily_search_tool = Tool(
    name="web_search",
    description=TAVILY_TOOL_DESCRIPTION,
    func=web_search
)
