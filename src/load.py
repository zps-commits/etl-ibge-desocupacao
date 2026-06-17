import os
from dotenv import load_dotenv
from pymongo import MongoClient, UpdateOne
from pymongo.server_api import ServerApi

load_dotenv()


class Load:
    def __init__(self, mongo_uri=None):
        self.mongo_uri = mongo_uri or os.getenv("MONGO_URI")

    def insert_in_mongo(self, documentos, db_name, collection_name):
        """Grava documentos no MongoDB com upsert. Chave: indicador+categoria+periodo+localidade."""
        if not self.mongo_uri:
            raise ValueError("A variável MONGO_URI não foi encontrada no arquivo .env")

        client = MongoClient(self.mongo_uri, server_api=ServerApi("1"))

        try:
            client.admin.command("ping")
            print("Conectado ao MongoDB Atlas com sucesso!")

            db = client[db_name]
            collection = db[collection_name]

            # Remove índices antigos se existirem
            for nome_idx in ("idx_categoria_periodo", "idx_indicador_categoria_periodo"):
                try:
                    collection.drop_index(nome_idx)
                except Exception:
                    pass

            collection.create_index(
                [("indicador", 1), ("categoria", 1), ("periodo", 1), ("localidade", 1)],
                unique=True,
                name="idx_indicador_categoria_periodo_localidade",
            )

            if not documentos:
                print("Nenhum documento para inserir.")
                return

            operacoes = []
            for doc in documentos:
                filtro = {
                    "indicador": doc["indicador"],
                    "categoria": doc["categoria"],
                    "periodo": doc["periodo"],
                    "localidade": doc["localidade"],
                }
                operacoes.append(UpdateOne(filtro, {"$set": doc}, upsert=True))

            resultado = collection.bulk_write(operacoes)

            print(f"Inseridos: {resultado.upserted_count}")
            print(f"Atualizados: {resultado.modified_count}")
            print(f"Total de documentos na coleção: {collection.count_documents({})}")

        except Exception as e:
            print(f"Erro: {e}")
            raise
        finally:
            client.close()
