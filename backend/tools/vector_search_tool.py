from langchain_core.tools import tool
from langchain_core.embeddings.embeddings import Embeddings
from langchain_community.vectorstores import SupabaseVectorStore
from supabase.client import create_client
from sentence_transformers import SentenceTransformer

class SentenceEmbeddings(Embeddings):
    def __init__(self):
        self.model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

    def embed_documents(self, texts: list[str]) -> list[list[float]]:
        return [self.encode(text) for text in texts]
    
    def embed_query(self, text: str) -> list[float]:
        return self.model.encode(text)

@tool
def vector_search_tool(query: str):
    """
    Search the vector database with research papers about expoplanets.
    
    Args:
        query (str): The search query to execute
    """
    supabase_client = create_client("my_supabase_url", "my_supabase_key")
    embeddings = SentenceEmbeddings()
    vector_store = SupabaseVectorStore(
        client=supabase_client,
        embedding=embeddings,
        table_name="documents",
        query_name="match_documents",
    )

    results = vector_store.similarity_search(query)

    return results