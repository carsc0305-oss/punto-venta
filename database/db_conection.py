import sqlite3
import os

from config import DB_PATH, SCHEMA_PATH


def conectar_db():

    # Crear el directorio de la base de datos si no existe
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)

    # Crear e inicializar la base de datos si no existe
    if not os.path.exists(DB_PATH):
        inicializar_db()

    return sqlite3.connect(DB_PATH, timeout=10)


def inicializar_db():

    # Crear el directorio por seguridad
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)

    # Leer el esquema SQL
    with open(SCHEMA_PATH, "r", encoding="utf-8") as f:
        schema = f.read()

    # Ejecutar el esquema
    with sqlite3.connect(DB_PATH, timeout=10) as conn:

        cursor = conn.cursor()

        cursor.executescript(schema)

        conn.commit()

    print("DB inicializada correctamente.")