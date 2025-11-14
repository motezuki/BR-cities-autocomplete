"""
API para consultar e trabalhar com o banco de dados SQLite de municípios.
Fornece funções úteis para análise e busca de dados.
"""

import utils
import fastapi
from fastapi.middleware.cors import CORSMiddleware
from mangum import Mangum
import uvicorn

DB_FILE = "xls2sqlite/municipios_brasil.db"
TABLE_NAME = "municipios"

app = fastapi.FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["*"],
)


@app.get("/")
def read_root():
    return {"message": "Hello from AWS Lambda using Python!"}


@app.get("/cidades")
def listar_cidades(limit: int = 100):
    """Lista cidades do banco de dados"""
    conn = utils.connectar_db()
    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM {TABLE_NAME} LIMIT ?", (limit,))
    cidades = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return cidades


@app.get("/autocompletar")
def autocompletar_cidades(q: str, limit: int = 10):
    """Autocompleta nomes de cidades com base na consulta"""

    # Requer no mínimo 3 caracteres para busca
    if len(q) < 3:
        return {"total": 0, "cidades": []}

    conn = utils.connectar_db()
    cursor = conn.cursor()

    # Normaliza consulta do usuário
    q_norm = utils.normaliza_string(q)
    # Busca usando a coluna normalizada (prefix match)
    sql = f"SELECT Nome_Município, UF FROM {TABLE_NAME} WHERE nome_normalizado LIKE ? ORDER BY nome_normalizado ASC LIMIT ?"
    cursor.execute(sql, (f"{q_norm}%", limit))
    cidades = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return {"total": len(cidades), "cidades": cidades}


def handler(event, context):
    """
    AWS Lambda handler
    """
    # Create and call Mangum handler with explicit settings
    asgi_handler = Mangum(
        app,
        lifespan="off",
        api_gateway_base_path="",
    )
    return asgi_handler(event, context)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)
