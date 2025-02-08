import sqlite3
import numpy as np
import os
import openai
import tiktoken  # biblioteka do pracy z tokenami
from tqdm import tqdm  # 🔹 Pasek postępu
from dotenv import load_dotenv

# 🔹 Załaduj zmienne środowiskowe z pliku .env
load_dotenv()

# --- KONFIGURACJA ---
TXT_DIR = "./downloaded_pdfs"            # Katalog z plikami TXT
CHUNK_TOKENS = 1000                      # Rozmiar chunku w tokenach
CHUNK_OVERLAP = 50                       # Ile tokenów ma nachodzić na kolejny chunk
OPENAI_MODEL = "text-embedding-ada-002"  # Model OpenAI do embeddowania

# 🔹 Pobierz klucz API i inicjalizuj klienta OpenAI (dla wersji 1.0.0+)
api_key = os.getenv("OPENAI_API_KEY")
client = openai.OpenAI(api_key=api_key)

# --- Funkcja do dzielenia tekstu na fragmenty według tokenów ---
def chunk_text_by_tokens(text, tokens_per_chunk=CHUNK_TOKENS, overlap=CHUNK_OVERLAP, model_name=OPENAI_MODEL):
    """
    Dzieli tekst na fragmenty o długości określonej liczbą tokenów (tokens_per_chunk).
    Dodaje overlap (wspólną liczbę tokenów) między kolejnymi fragmentami.
    """
    try:
        encoding = tiktoken.encoding_for_model(model_name)
    except KeyError:
        encoding = tiktoken.get_encoding("cl100k_base")

    tokens = encoding.encode(text)  # Zamieniamy cały tekst na listę tokenów
    chunks = []
    start = 0

    while start < len(tokens):
        end = start + tokens_per_chunk
        chunk_slice = tokens[start:end]
        chunk_text = encoding.decode(chunk_slice)
        chunks.append(chunk_text)
        start += tokens_per_chunk - overlap  # Przesunięcie z overlapem

    return chunks

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
    exit(0)

print(f"🔍 Znaleziono {len(files)} plików TXT do wektoryzacji.")

# --- Główna pętla: odczyt plików, dzielenie, generowanie embeddingów, zapis do DB ---
for file in tqdm(files, desc="📂 Przetwarzanie plików"):
    file_path = os.path.join(TXT_DIR, file)
    
    if not os.path.exists(file_path):
        print(f"⚠️ Plik nie istnieje: {file_path}")
        continue
    
    # Odczytujemy tekst z pliku
    with open(file_path, "r", encoding="utf-8") as f:
        text = f.read().strip()

    if not text:
        print(f"⚠️ Plik jest pusty: {file_path}")
        continue

    # Dzielimy tekst według tokenów z overlapem
    chunks = chunk_text_by_tokens(text, CHUNK_TOKENS, CHUNK_OVERLAP, OPENAI_MODEL)

    # Pasek postępu dla embeddingów
    for i, chunk in enumerate(tqdm(chunks, desc=f"🔹 {file}", leave=False)):
        response = client.embeddings.create(input=chunk, model=OPENAI_MODEL)
        vector = np.array(response.data[0].embedding, dtype=np.float32)
        vector_blob = vector.tobytes()
        
        cursor.execute(
            "INSERT INTO document_vectors (filename, chunk_index, text_snippet, vector) VALUES (?, ?, ?, ?)",
            (file, i, chunk[:200], vector_blob)
        )

conn.commit()
conn.close()

print("✅ Nowe wektory zapisane do SQLite z wykorzystaniem chunkowania po tokenach i overlapu!")