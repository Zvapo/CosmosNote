import sqlite3
import numpy as np
import os
import openai
import tiktoken  # biblioteka do pracy z tokenami
from dotenv import load_dotenv

# Załaduj zmienne środowiskowe z pliku .env
load_dotenv()

# --- KONFIGURACJA ---
TXT_DIR = "./downloaded_pdfs"            # Katalog z plikami TXT
CHUNK_TOKENS = 1000                      # Rozmiar chunku w tokenach
CHUNK_OVERLAP = 50                       # Ile tokenów ma nachodzić na kolejny chunk
OPENAI_MODEL = "text-embedding-ada-002"  # Model OpenAI do embeddowania

# Pobierz klucz API z zmiennych środowiskowych lub wpisz bezpośrednio
openai.api_key = os.getenv("OPENAI_API_KEY")

# --- Funkcja do dzielenia tekstu na fragmenty według tokenów ---
def chunk_text_by_tokens(text, tokens_per_chunk=CHUNK_TOKENS, overlap=CHUNK_OVERLAP, model_name=OPENAI_MODEL):
    """
    Dzieli tekst na fragmenty o długości określonej liczbą tokenów (tokens_per_chunk).
    Dodaje overlap (wspólną liczbę tokenów) między kolejnymi fragmentami.
    """
    # Odczytujemy enkoder dopasowany do danego modelu (lub np. 'cl100k_base')
    try:
        encoding = tiktoken.encoding_for_model(model_name)
    except KeyError:
        # W razie problemów z rozpoznaniem modelu, można użyć domyślnego:
        encoding = tiktoken.get_encoding("cl100k_base")

    # Zamieniamy cały tekst na listę tokenów
    tokens = encoding.encode(text)

    chunks = []
    start = 0

    # Dopóki nie osiągniemy końca listy tokenów, wycinamy fragment
    while start < len(tokens):
        end = start + tokens_per_chunk
        chunk_slice = tokens[start:end]

        # Dekodujemy tokeny z powrotem do ciągu tekstowego
        chunk_text = encoding.decode(chunk_slice)
        chunks.append(chunk_text)

        # Przesuwamy "okno" chunku w prawo, ale część (overlap) się nakłada
        start += tokens_per_chunk - overlap

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
else:
    print(f"🔍 Znaleziono {len(files)} plików TXT do wektoryzacji.")

# --- Główna pętla: odczyt plików, dzielenie, generowanie embeddingów, zapis do DB ---
for file in files:
    file_path = os.path.join(TXT_DIR, file)
    
    if not os.path.exists(file_path):
        print(f"⚠️ Plik nie istnieje: {file_path}")
        continue  # Pomijamy plik, jeśli nie istnieje
    
    # Odczytujemy tekst z pliku
    with open(file_path, "r", encoding="utf-8") as f:
        text = f.read().strip()

    if not text:  # Jeśli plik jest pusty, pomijamy
        print(f"⚠️ Plik jest pusty: {file_path}")
        continue

    # Dzielimy tekst według tokenów z overlapem
    chunks = chunk_text_by_tokens(text, CHUNK_TOKENS, CHUNK_OVERLAP, OPENAI_MODEL)

    # Dla każdego chunka – generujemy embedding, zapis do bazy
    for i, chunk in enumerate(chunks):
        response = openai.Embedding.create(input=chunk, model=OPENAI_MODEL)
        vector = np.array(response["data"][0]["embedding"], dtype=np.float32)
        vector_blob = vector.tobytes()
        
        # Zachowujemy fragment tekstu (np. do 200 znaków) jako "podgląd"
        cursor.execute(
            "INSERT INTO document_vectors (filename, chunk_index, text_snippet, vector) VALUES (?, ?, ?, ?)",
            (file, i, chunk[:200], vector_blob)
        )

conn.commit()
conn.close()

print("✅ Nowe wektory zapisane do SQLite z wykorzystaniem chunkowania po tokenach i overlapu!")