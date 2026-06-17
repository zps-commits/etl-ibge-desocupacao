import sys
from prefect import flow, task, get_run_logger
from src.extract import Extract
from src.transform import Transform
from src.load import Load


@task(name="📡 Extrair Dados do IBGE", retries=3, retry_delay_seconds=10)
def extract_ibge() -> list:
    logger = get_run_logger()
    extractor = Extract()
    dados = extractor.extract_indicadores()
    logger.info(f"JSON cru retornado com {len(dados)} variáveis")
    return dados


@task(name="⚙️ Transformar Dados")
def transform_ibge(dados_brutos: list) -> list:
    logger = get_run_logger()
    transformador = Transform()
    documentos = transformador.transform(dados_brutos)
    logger.info(f"{len(documentos)} documentos normalizados")
    return documentos


@task(name="🍃 Carregar no MongoDB Atlas", retries=2, retry_delay_seconds=15)
def load_ibge(documentos: list, db_name: str, collection_name: str):
    logger = get_run_logger()
    loader = Load()
    loader.insert_in_mongo(documentos, db_name, collection_name)
    logger.info(f"{len(documentos)} registros processados em {db_name}.{collection_name}")


@flow(name="🇧🇷 Pipeline ETL · IBGE Desocupação", log_prints=True)
def etl_ibge_desocupacao_flow():
    dados = extract_ibge()
    documentos = transform_ibge(dados)
    load_ibge(documentos, "desocupacao", "taxa_desocupacao")


if __name__ == "__main__":
    if "--deploy" in sys.argv:
        # Agendamento trimestral: dia 1 de jan, abr, jul e out às 06:00 UTC
        etl_ibge_desocupacao_flow.serve(
            name="etl-ibge-trimestral",
            cron="0 6 1 1,4,7,10 *",
        )
    else:
        etl_ibge_desocupacao_flow()
