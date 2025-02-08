import sqlite3
import numpy as np
import os
from sentence_transformers import SentenceTransformer

# --- Ładowanie poprawnego modelu (384 wymiary) ---
MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"
model = SentenceTransformer(MODEL_NAME)

# --- Połączenie z bazą danych ---
conn = sqlite3.connect("vectors.db")
cursor = conn.cursor()

# --- Tworzenie tabeli (jeśli nie istnieje) ---
cursor.execute("""
CREATE TABLE IF NOT EXISTS document_vectors (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    filename TEXT,
    text_snippet TEXT,
    vector BLOB
)
""")

# --- Ścieżka do katalogu z plikami TXT ---
TXT_DIR = "./downloaded_pdfs"

# --- Automatyczne pobieranie nazw plików TXT ---
files = [f for f in os.listdir(TXT_DIR) if f.endswith(".txt")]

if not files:
    print("⚠️ Brak plików TXT w katalogu!")
else:
    print(f"🔍 Znaleziono {len(files)} plików TXT do wektoryzacji.")

for file in files:
    file_path = os.path.join(TXT_DIR, file)
    
    if not os.path.exists(file_path):
        print(f"⚠️ Plik nie istnieje: {file_path}")
        continue  # Pomijamy plik, jeśli nie istnieje
    
    with open(file_path, "r", encoding="utf-8") as f:
        text = f.read()
    
    if not text.strip():  # Jeśli plik jest pusty, pomijamy
        print(f"⚠️ Plik jest pusty: {file_path}")
        continue

    vector = model.encode(text)  # ✅ Generuje poprawny wymiar (384,)
    vector_blob = vector.tobytes()  # Konwersja do formatu BLOB
    
    cursor.execute("INSERT INTO document_vectors (filename, text_snippet, vector) VALUES (?, ?, ?)",
                   (file, text[:200], vector_blob))

conn.commit()
conn.close()

print("✅ Nowe wektory (384D) zapisane do SQLite!")