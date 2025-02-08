from langchain_community.tools.tavily_search import TavilySearchResults
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get Tavily API key from environment
tavily_api_key = os.getenv("TAVILY_API_KEY")
if not tavily_api_key:
    raise ValueError("TAVILY_API_KEY environment variable is not set")

# Initialize the search tool with the API key
web_search_tool = TavilySearchResults(
    tavily_api_key=tavily_api_key,  # Explicitly pass the API key
    max_results=2,
    include_raw_content=True,
    include_images=False
)