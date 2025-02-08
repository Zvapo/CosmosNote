import sqlite3
import numpy as np
import psycopg2
from psycopg2.extras import execute_values

# --- KONFIGURACJA SUPABASE (PostgreSQL) ---
DB_NAME = "postgres"
DB_USER = "postgres.ezlovmsmtdengapiohfz"
DB_PASSWORD = "Kepler-LOL42_GasGiant!"
DB_HOST = "aws-0-eu-central-1.pooler.supabase.com"
DB_PORT = "6543"
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
    vector FLOAT8[]
)
""")
conn_pg.commit()

# --- Przygotowanie danych do batch insert ---
data = []
for row in rows:
    filename, text_snippet, vector_blob = row
    vector = np.frombuffer(vector_blob, dtype=np.float32).tolist()  # Konwersja na listę floatów (Postgres obsługuje FLOAT8[])
    
    data.append((filename, text_snippet, vector))

if data:
    # Batch insert do Supabase (szybsze niż pojedyncze INSERTy)
    query = f"INSERT INTO {TABLE_NAME} (filename, text_snippet, vector) VALUES %s"
    execute_values(cursor_pg, query, data)

    conn_pg.commit()
    print(f"✅ Przesłano {len(data)} wektorów do Supabase!")

# --- Zamknięcie połączeń ---
cursor_sqlite.close()
conn_sqlite.close()
cursor_pg.close()
conn_pg.close()

print("🎯 Wszystkie dane zostały przesłane do Supabase PostgreSQL!")