from src.extract import Extract
from src.transform import Transform
from src.load import Load
from datetime import datetime, timezone

ext = Extract()
trf = Transform()
ld = Load()

print("=" * 50)
print("ETL - Indicadores de Emprego IBGE (PNAD Contínua)")
print(f"Início: {datetime.now(timezone.utc).isoformat()}")
print("=" * 50)

print("\n[1/3] Extraindo dados da API do IBGE...")
dados_brutos = ext.extract_indicadores()

print("\n[2/3] Transformando dados...")
documentos = trf.transform(dados_brutos)

indicadores = set(d["indicador"] for d in documentos)
categorias = set(d["categoria"] for d in documentos)
print(f"Total de registros: {len(documentos)}")
print(f"Indicadores: {', '.join(indicadores)}")
print(f"Categorias: {', '.join(categorias)}")

print("\n[3/3] Carregando dados no MongoDB Atlas...")
ld.insert_in_mongo(documentos, "desocupacao", "taxa_desocupacao")

print("\nETL concluída com sucesso!")
