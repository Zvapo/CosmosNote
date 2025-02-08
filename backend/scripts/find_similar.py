import sqlite3
import numpy as np
from sentence_transformers import SentenceTransformer

# --- Model do enkodowania zapytań ---
MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"
model = SentenceTransformer(MODEL_NAME)

# --- Połączenie z bazą SQLite ---
DB_PATH = "vectors.db"

def find_similar(query, top_n=5):
    """Znajduje najbliższe dokumenty dla podanego zapytania"""
    
    # 🔹 Enkodowanie zapytania do wektora (384D)
    query_vector = model.encode(query)

    # 🔹 Połączenie z bazą
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # 🔹 Pobranie wszystkich wektorów z bazy
    cursor.execute("SELECT id, filename, text_snippet, vector FROM document_vectors")
    rows = cursor.fetchall()
    
    similarities = []
    
    for row in rows:
        doc_id, filename, text_snippet, vector_blob = row
        doc_vector = np.frombuffer(vector_blob, dtype=np.float32)  # Konwersja BLOB → NumPy
        
        if doc_vector.shape[0] != query_vector.shape[0]:
            print(f"⚠️ Rozmiar wektora w bazie (({doc_vector.shape[0]},)) nie pasuje do modelu (({query_vector.shape[0]},)). Pomijam...")
            continue

        # 🔹 Obliczanie podobieństwa kosinusowego
        similarity = np.dot(doc_vector, query_vector) / (np.linalg.norm(doc_vector) * np.linalg.norm(query_vector))
        similarities.append((similarity, filename, text_snippet))
    
    conn.close()

    # 🔹 Sortowanie po podobieństwie malejąco
    similarities.sort(reverse=True, key=lambda x: x[0])
    
    # 🔹 Zwrócenie `top_n` najbardziej podobnych dokumentów
    return similarities[:top_n]


# --- TEST WYSZUKIWANIA ---
if __name__ == "__main__":
    query = input("🔍 Wpisz zapytanie: ")
    results = find_similar(query)

    print("\n🎯 Najbardziej podobne dokumenty:\n")
    for score, filename, snippet in results:
        print(f"📄 {filename} ({score:.4f})")
        print(f"   📝 {snippet[:150]}...\n")  # Wyświetla fragment tekstu dla kontekstu