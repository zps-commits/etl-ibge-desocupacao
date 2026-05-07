from dotenv import load_dotenv
import os
from pymongo import MongoClient
from pymongo.server_api import ServerApi

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")


class Load:
    def __init__(self):
        pass

    def insert_in_mongo(self, records, db_name, collection_name):
        if not MONGO_URI:
            raise ValueError("A variável MONGO_URI não foi encontrada no arquivo .env")

        client = MongoClient(MONGO_URI, server_api=ServerApi("1"))
        db = client[db_name]
        collection = db[collection_name]

        if records:
            if isinstance(records, list):
                collection.insert_many(records)
            else:
                collection.insert_one(records)

        print(f"Dados inseridos com sucesso na coleção '{collection_name}'!")
        client.close()
