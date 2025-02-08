import sqlite3
import numpy as np
import openai
import os
from dotenv import load_dotenv

# 🔹 Load API key from .env file
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

# 🔹 OpenAI client setup (new API format)
client = openai.OpenAI(api_key=api_key)

# 🔹 OpenAI model
OPENAI_MODEL = "text-embedding-ada-002"

# 🔹 SQLite database path
DB_PATH = "vectors.db"

def get_embedding(text):
    """Generates embedding using OpenAI's API (new 1.0+ format)."""
    response = client.embeddings.create(
        input=text,
        model=OPENAI_MODEL
    )
    return np.array(response.data[0].embedding, dtype=np.float32)  # OpenAI returns a float list

def find_similar(query, top_n=5):
    """Finds the most similar documents in the database."""
    
    # 🔹 Generate embedding for the query (1536D vector)
    query_vector = get_embedding(query)

    # 🔹 Connect to the database
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # 🔹 Retrieve all vectors from the database
    cursor.execute("SELECT id, filename, text_snippet, vector FROM document_vectors")
    rows = cursor.fetchall()
    
    similarities = []
    
    for row in rows:
        doc_id, filename, text_snippet, vector_blob = row
        doc_vector = np.frombuffer(vector_blob, dtype=np.float32)  # Convert BLOB → NumPy
        
        if doc_vector.shape[0] != query_vector.shape[0]:
            print(f"⚠️ Vector size mismatch! DB: {doc_vector.shape[0]}, Query: {query_vector.shape[0]}. Skipping...")
            continue

        # 🔹 Compute cosine similarity
        similarity = np.dot(doc_vector, query_vector) / (np.linalg.norm(doc_vector) * np.linalg.norm(query_vector))
        similarities.append((similarity, filename, text_snippet))
    
    conn.close()

    # 🔹 Sort by similarity (descending order)
    similarities.sort(reverse=True, key=lambda x: x[0])
    
    # 🔹 Return top `n` most similar documents
    return similarities[:top_n]

# --- TEST SEARCH ---
if __name__ == "__main__":
    query = input("🔍 Enter query: ")
    results = find_similar(query)

    print("\n🎯 Most similar documents:\n")
    for score, filename, snippet in results:
        print(f"📄 {filename} ({score:.4f})")
        print(f"   📝 {snippet[:150]}...\n")  # Display a snippet of the text for context