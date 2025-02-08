import sqlite3
import numpy as np

DB_FILE = "vectors.db"

conn = sqlite3.connect(DB_FILE)
cursor = conn.cursor()

# Pobranie pierwszego wektora i sprawdzenie jego rozmiaru
cursor.execute("SELECT vector FROM document_vectors LIMIT 1")
row = cursor.fetchone()

if row:
    doc_vector = np.frombuffer(row[0], dtype=np.float32)
    print(f"📊 Rozmiar wektora w bazie: {doc_vector.shape}")
else:
    print("⚠️ Brak wektorów w bazie!")

conn.close()