import sqlite3
import numpy as np
import os
from sentence_transformers import SentenceTransformer

# --- KONFIGURACJA ---
MODEL_NAME = "sentence-transformers/all-mpnet-base-v2"  # 768D
model = SentenceTransformer(MODEL_NAME)

TXT_DIR = "./downloaded_pdfs"  # Katalog z plikami TXT
CHUNK_SIZE = 512  # Rozmiar pojedynczego fragmentu tekstu

# --- Połączenie z bazą danych ---
conn = sqlite3.connect("vectors.db")
cursor = conn.cursor()

# --- Tworzenie tabeli (jeśli nie istnieje) ---
cursor.execute("""
CREATE TABLE IF NOT EXISTS document_vectors (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    filename TEXT,
    chunk_index INTEGER,
    text_snippet TEXT,
    vector BLOB
)
""")

# --- Automatyczne pobieranie plików TXT ---
files = [f for f in os.listdir(TXT_DIR) if f.endswith(".txt")]

if not files:
    print("⚠️ Brak plików TXT w katalogu!")
else:
    print(f"🔍 Znaleziono {len(files)} plików TXT do wektoryzacji.")

# --- Funkcja do dzielenia tekstu na fragmenty ---
def chunk_text(text, chunk_size):
    """Dzieli tekst na mniejsze fragmenty o zadanej długości."""
    return [text[i:i+chunk_size] for i in range(0, len(text), chunk_size)]

# --- Wektoryzacja plików TXT ---
for file in files:
    file_path = os.path.join(TXT_DIR, file)
    
    if not os.path.exists(file_path):
        print(f"⚠️ Plik nie istnieje: {file_path}")
        continue  # Pomijamy plik, jeśli nie istnieje
    
    with open(file_path, "r", encoding="utf-8") as f:
        text = f.read().strip()

    if not text:  # Jeśli plik jest pusty, pomijamy
        print(f"⚠️ Plik jest pusty: {file_path}")
        continue

    chunks = chunk_text(text, CHUNK_SIZE)

    for i, chunk in enumerate(chunks):
        vector = model.encode(chunk)  # ✅ Generuje poprawny wymiar (768,)
        vector_blob = vector.tobytes()  # Konwersja do formatu BLOB
        
        cursor.execute("INSERT INTO document_vectors (filename, chunk_index, text_snippet, vector) VALUES (?, ?, ?, ?)",
                       (file, i, chunk[:200], vector_blob))

conn.commit()
conn.close()

print("✅ Nowe wektory (768D) zapisane do SQLite z chunkowaniem!")