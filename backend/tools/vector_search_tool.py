import os
from langchain_core.tools import tool
from langchain_core.embeddings.embeddings import Embeddings
from langchain_community.vectorstores import SupabaseVectorStore
from supabase.client import create_client
from sentence_transformers import SentenceTransformer
from dotenv import load_dotenv


load_dotenv()


class SentenceEmbeddings(Embeddings):
    def __init__(self):
        self.model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

    def embed_documents(self, texts: list[str]) -> list[list[float]]:
        embeddings = self.model.encode(texts)
        return embeddings.tolist()
    
    def embed_query(self, text: str) -> list[float]:
        embedding = self.model.encode(text)
        return embedding.tolist()


supabase_client = create_client(os.getenv("SUPABASE_URL"), os.getenv("SUPABASE_API_KEy"))
embeddings = SentenceEmbeddings()
vector_store = SupabaseVectorStore(
    client=supabase_client,
    embedding=embeddings,
    table_name="document_vectors_test",
    query_name="match_documents",
)

@tool
def vector_search_tool(query: str):
    """
    Search the vector database with research papers about expoplanets.
    
    Args:
        query (str): The search query to execute
    """
    results = vector_store.similarity_search(query)

    return results


if __name__ == "__main__":
    print(vector_search_tool.invoke({"query": "How does the redder TESS bandpass affect oscillation amplitude compared to Kepler?"}))
