from langchain_core.tools import tool

@tool
def vector_search_tool(query: str):
    """
    Search the vector database with research papers about expoplanets.
    
    Args:
        query (str): The search query to execute
    """
    return "hello this is a test"