import sqlite3
import numpy as np
import psycopg2
from psycopg2.extras import execute_values
from tqdm import tqdm  # Pasek postępu

# --- KONFIGURACJA SUPABASE (PostgreSQL) ---
DB_NAME = os.getenv('DB_NAME')
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_HOST = os.getenv('DB_HOST')
DB_PORT = os.getenv('DB_PORT')
TABLE_NAME = "document_vectors"  # Nazwa tabeli w Supabase

# --- Połączenie z lokalną bazą SQLite ---
conn_sqlite = sqlite3.connect("vectors.db")
cursor_sqlite = conn_sqlite.cursor()

# --- Pobranie wszystkich wektorów ---
cursor_sqlite.execute("SELECT filename, text_snippet, vector FROM document_vectors")
rows = cursor_sqlite.fetchall()

# --- Połączenie z bazą PostgreSQL (Supabase) ---
conn_pg = psycopg2.connect(
    dbname=DB_NAME,
    user=DB_USER,
    password=DB_PASSWORD,
    host=DB_HOST,
    port=DB_PORT
)
cursor_pg = conn_pg.cursor()

# --- Tworzenie tabeli w Supabase (jeśli nie istnieje) ---
cursor_pg.execute(f"""
CREATE TABLE IF NOT EXISTS {TABLE_NAME} (
    id SERIAL PRIMARY KEY,
    filename TEXT,
    text_snippet TEXT,
    vector VECTOR(1536)  -- Obsługa nowego wymiaru dla text-embedding-ada-002
)
""")
conn_pg.commit()

# --- Przygotowanie danych do batch insert ---
data = []
print("🔄 Pobieranie danych z SQLite...")
for row in tqdm(rows, desc="📂 Przetwarzanie wektorów", unit="vec"):
    filename, text_snippet, vector_blob = row

    # Usunięcie NULL (\x00) z tekstu
    text_snippet = text_snippet.replace("\x00", " ") if text_snippet else ""
    
    # Konwersja z SQLite (binary blob) na listę floatów
    vector = np.frombuffer(vector_blob, dtype=np.float32).tolist()
    
    # Sprawdzenie poprawności wymiaru (powinno być 1536D)
    if len(vector) != 1536:
        print(f"⚠️ Wektor dla {filename} ma niepoprawny wymiar: {len(vector)}")
        continue  # Pomijamy błędne dane

    data.append((filename, text_snippet, vector))

if data:
    print("🚀 Wysyłanie danych do Supabase...")
    query = f"INSERT INTO {TABLE_NAME} (filename, text_snippet, vector) VALUES %s"

    # Dodajemy pasek postępu dla batch insert
    batch_size = 500  # Wstawiamy po 500 rekordów dla optymalizacji
    for i in tqdm(range(0, len(data), batch_size), desc="📤 Wysyłanie batchy", unit="batch"):
        batch = data[i:i+batch_size]
        execute_values(cursor_pg, query, batch)
        conn_pg.commit()

    print(f"✅ Przesłano {len(data)} wektorów do Supabase!")

# --- Zamknięcie połączeń ---
cursor_sqlite.close()
conn_sqlite.close()
cursor_pg.close()
conn_pg.close()

print("🎯 Wszystkie dane zostały przesłane do Supabase PostgreSQL!")