"""
API para consultar e trabalhar com o banco de dados SQLite de municípios.
Fornece funções úteis para análise e busca de dados.
"""

import fastapi
from mangum import Mangum
import uvicorn

app = fastapi.FastAPI()


@app.get("/")
def read_root():
    return {"message": "Hello from AWS Lambda using Python!"}


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
