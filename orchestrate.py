from prefect import flow, task, get_run_logger
from src.extract import Extract
from src.load import Load

@task(retries=3, retry_delay_seconds=10)
def extract_ibge() -> list[dict]:
    logger = get_run_logger()
    extractor = Extract()
    data = extractor.extract_taxa_desocupacao()
    logger.info(f"{len(data)} registros extraídos do IBGE")
    return data

@task
def load_ibge_data(records, db_name: str, collection_name: str):
    logger = get_run_logger()
    loader = Load()
    loader.insert_in_mongo(records, db_name, collection_name)
    logger.info(f"{len(records)} registros inseridos em {db_name}.{collection_name}")

@flow(name="ETL IBGE Desocupacao Prefect", log_prints=True)
def etl_ibge_desocupacao_flow():
    data = extract_ibge()
    load_ibge_data(data, "desocupacao", "taxa_desocupacao")

if __name__ == "__main__":
    etl_ibge_desocupacao_flow()
