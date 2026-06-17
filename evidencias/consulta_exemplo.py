"""
Consulta real ao MongoDB Atlas:
taxa de desocupação das mulheres em Pernambuco no último trimestre disponível.
"""
import os
import certifi
from dotenv import load_dotenv
from pymongo import MongoClient
from pymongo.server_api import ServerApi

load_dotenv()

client = MongoClient(
    os.getenv("MONGO_URI"),
    server_api=ServerApi("1"),
    tlsCAFile=certifi.where(),
)

col = client["desocupacao"]["taxa_desocupacao"]

doc = col.find_one(
    {
        "indicador": "taxa_desocupacao",
        "categoria": "Mulheres",
        "localidade": "Pernambuco",
    },
    sort=[("periodo", -1)],
)

if doc:
    print(f"Indicador : {doc['indicador']}")
    print(f"Localidade: {doc['localidade']}")
    print(f"Categoria : {doc['categoria']}")
    print(f"Período   : {doc['periodo'][:4]}T{doc['periodo'][4:]}")
    print(f"Valor     : {doc['valor']}%")
    print(f"Coletado  : {doc.get('data_coleta', 'N/A')}")
else:
    print("Nenhum documento encontrado.")

client.close()
