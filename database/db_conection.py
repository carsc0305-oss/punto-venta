import sqlite3
from config import DB_PATH, SCHEMA_PATH
import os

def conectar_db():
    # Crear la base de datos si no existe y tambien el directorio donde se encuentra
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    if not os.path.exists(DB_PATH):
        inicializar_db()
        
    return sqlite3.connect(DB_PATH, timeout=10)

def inicializar_db():
    with open(SCHEMA_PATH, 'r', encoding='utf-8') as f:
        schema = f.read()

    with sqlite3.connect(DB_PATH, timeout=10) as conn:
        cursor = conn.cursor()
        cursor.executescript(schema)
        conn.commit()
        print("DB inicializada correctamente.")