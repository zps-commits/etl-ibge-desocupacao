import sqlite3
from dotenv import load_dotenv
import os
from pymongo import MongoClient
from pymongo.server_api import ServerApi

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")


class Load:
    def __init__(self):
        pass

    def create_sqlite_table(self, universities_list, db_name, table_name):
        con = sqlite3.connect(f"{db_name}.db")
        c = con.cursor()

        c.execute(f"""
        CREATE TABLE IF NOT EXISTS {table_name}
                (
                id INTEGER PRIMARY KEY,
                name TEXT,
                country TEXT,
                state_province TEXT,
                web_pages TEXT,
                domains TEXT
                );
        """)

        for university in universities_list:
            c.execute(
                f"""INSERT INTO {table_name} (name, country, state_province, web_pages, domains) VALUES (?,?,?,?,?);""",
                (
                    university.get("name"),
                    university.get("country"),
                    university.get("state-province"),
                    ", ".join(university.get("web_pages", [])),
                    ", ".join(university.get("domains", [])),
                ),
            )

        con.commit()
        con.close()

    def insert_in_mongo(self, uni_dict, db_name, collection_name):
        if not MONGO_URI:
            raise ValueError("A variável MONGO_URI não foi encontrada no arquivo .env")

        client = MongoClient(MONGO_URI, server_api=ServerApi("1"))

        db = client[db_name]
        collection = db[collection_name]

        if uni_dict:
            if isinstance(uni_dict, list):
                collection.insert_many(uni_dict)
            else:
                collection.insert_one(uni_dict)

        print(f"Dados inseridos com sucesso na coleção '{collection_name}'!")
        client.close()
