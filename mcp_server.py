from fastmcp import FastMCP
from pymongo import MongoClient
from pymongo.server_api import ServerApi
from dotenv import load_dotenv
import os

load_dotenv()

mcp = FastMCP("ibge-desocupacao")

MONGO_URI = os.getenv("MONGO_URI")


def _get_collection():
    client = MongoClient(MONGO_URI, server_api=ServerApi("1"))
    return client["desocupacao"]["taxa_desocupacao"]


@mcp.tool()
def buscar_indicadores_pnad(
    indicador: str = None,
    localidade: str = None,
    categoria: str = None,
    periodo: str = None,
) -> list:
    """
    Busca indicadores de emprego do IBGE (PNAD Contínua Trimestral) no MongoDB.

    Args:
        indicador: Variável desejada — 'taxa_desocupacao', 'taxa_participacao' ou 'taxa_informalidade'. Opcional.
        localidade: UF desejada, ex: 'Pernambuco'. Opcional.
        categoria: Sexo — 'Total', 'Homens' ou 'Mulheres'. Opcional.
        periodo: Período no formato YYYYT (ex: '20241' para 1º trim 2024). Use 'ultimo' para o trimestre mais recente. Opcional.

    Returns:
        Lista com os registros encontrados no MongoDB.
    """
    col = _get_collection()

    filtro = {"indicador": {"$exists": True}}

    if indicador:
        filtro["indicador"] = indicador
    if localidade:
        filtro["localidade"] = {"$regex": localidade, "$options": "i"}
    if categoria:
        filtro["categoria"] = {"$regex": categoria, "$options": "i"}

    if periodo == "ultimo":
        ultimo = col.find_one(
            {"indicador": {"$exists": True}},
            sort=[("periodo", -1)],
            projection={"periodo": 1}
        )
        if ultimo:
            filtro["periodo"] = ultimo["periodo"]
    elif periodo:
        filtro["periodo"] = periodo

    docs = list(col.find(filtro, {"_id": 0}).sort("periodo", -1).limit(100))
    return docs


if __name__ == "__main__":
    mcp.run()
