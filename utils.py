import sqlite3
import unicodedata

DB_FILE = "municipios_brasil.db"

def connectar_db(db_path: str = DB_FILE) -> sqlite3.Connection:
    """Conecta ao banco de dados SQLite"""
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row  # Permite acessar colunas por nome
    return conn
