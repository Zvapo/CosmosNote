import os
import psycopg2
import numpy as np
from dotenv import load_dotenv
import ast

# 🔹 Załaduj zmienne środowiskowe z pliku .env
load_dotenv()

# Pobranie danych uwierzytelniających z zmiennych środowiskowych
DB_NAME = os.getenv('DB_NAME')
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_HOST = os.getenv('DB_HOST')
DB_PORT = os.getenv('DB_PORT')

print(DB_NAME, DB_USER, DB_PASSWORD, DB_HOST, DB_PORT)

# Połączenie z bazą danych
conn = psycopg2.connect(
    dbname=DB_NAME,
    user=DB_USER,
    password=DB_PASSWORD,
    host=DB_HOST,
    port=DB_PORT
)
cursor = conn.cursor()

# Pobranie pierwszego wektora i sprawdzenie jego rozmiaru
cursor.execute("SELECT vector FROM document_vectors LIMIT 1")
row = cursor.fetchone()

if row:
    try:
        # Convert the string representation of a list into an actual list
        vector_list = ast.literal_eval(row[0])  # Safely parse the string as a list

        # Convert to NumPy array
        doc_vector = np.array(vector_list, dtype=np.float32)
        print(f"📊 Rozmiar wektora w bazie: {doc_vector.shape}")
    
    except (ValueError, SyntaxError) as e:
        print(f"❌ Błąd konwersji wektora: {e}")
else:
    print("⚠️ Brak wektorów w bazie!")

# Zamknięcie połączenia
cursor.close()
conn.close()