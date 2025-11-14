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
