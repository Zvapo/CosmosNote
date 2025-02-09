import sqlite3
import numpy as np
import os
import openai
from tqdm import tqdm  # Pasek postępu
from dotenv import load_dotenv
from langchain_text_splitters import RecursiveCharacterTextSplitter

# Załaduj zmienne środowiskowe
load_dotenv()

# --- KONFIGURACJA ---
TXT_DIR = "./downloaded_pdfs"            # Katalog z plikami TXT
CHUNK_TOKENS = 5000                        # Rozmiar chunku w tokenach
CHUNK_OVERLAP = 300                        # Ile tokenów ma nachodzić na kolejny chunk
OPENAI_MODEL = "text-embedding-3-large"  # Nowy model OpenAI do embeddowania

# Pobierz klucz API i inicjalizuj klienta OpenAI
api_key = os.getenv("OPENAI_API_KEY")
client = openai.OpenAI(api_key=api_key)

# Konfiguracja splittera tekstu
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=CHUNK_TOKENS,
    chunk_overlap=CHUNK_OVERLAP,
    separators=["\n\n", "\n", " ", "", ".", ",", "​", "，", "、", "．", "。"]
)

# --- Połączenie z bazą danych ---
conn = sqlite3.connect("vectors.db")
cursor = conn.cursor()

# Tworzenie tabeli (jeśli nie istnieje)
cursor.execute("""
CREATE TABLE IF NOT EXISTS document_vectors (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    filename TEXT,
    chunk_index INTEGER,
    text_snippet TEXT,
    vector BLOB
)
""")

# Pobieranie plików TXT
files = [f for f in os.listdir(TXT_DIR) if f.endswith(".txt")]

if not files:
    print("⚠️ Brak plików TXT w katalogu!")
    exit(0)

print(f"🔍 Znaleziono {len(files)} plików TXT do wektoryzacji.")

# Główna pętla: odczyt plików, dzielenie, generowanie embeddingów, zapis do DB
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

    # Dzielimy tekst na fragmenty
    chunks = text_splitter.split_text(text)

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

print("✅ Nowe wektory zapisane do SQLite z wykorzystaniem RecursiveCharacterTextSplitter!")
