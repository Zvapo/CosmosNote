import os
from langchain_core.tools import tool
from langchain_core.embeddings.embeddings import Embeddings
from langchain_community.vectorstores import SupabaseVectorStore
from langchain_openai import OpenAIEmbeddings
from supabase.client import create_client
from dotenv import load_dotenv


load_dotenv()


supabase_client = create_client(os.getenv("SUPABASE_URL"), os.getenv("SUPABASE_API_KEy"))
embeddings = OpenAIEmbeddings(model="text-embedding-ada-002")

@tool
def vector_search_tool(query: str) -> str:
    """
    This tools job is to search the vector database with research papers about exoplanets.
    Search the vector database as a researcher would do.
    Search the vector database for key words and phrases related to the query.
    Example queries:
    -What is the main subject of the document?
    -Which planet was discovered by TESS in this document?
    -What type of star is TOI-197 classified as?
    -What is the approximate radius of TOI-197?
    -How was TOI-197.01 characterized?
    -What is the significance of asteroseismology in this study?
    -What is the orbital period of TOI-197.01?
    -Which observatories provided high-resolution spectroscopy data for TOI-197?
    -How does the redder TESS bandpass affect oscillation amplitude compared to Kepler?
    
    Args:
        query (str): The search query to execute
        
    Returns:
        str: A string containing the search results
    """

    query_embedding = embeddings.embed_query(query)
    response = supabase_client.rpc("match_documents", {"query_embedding": query_embedding}).execute()
    docs = [doc["text_snippet"] for doc in response.data]
    # Convert the results to a string format
    formatted_results = "\n\n".join(docs)

    return formatted_results


if __name__ == "__main__":
    # Direct invocation without using dict
    query = "How does the redder TESS bandpass affect oscillation amplitude compared to Kepler?"
    print(vector_search_tool.invoke({ "query": query }))