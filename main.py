from src.extract import Extract
from src.load import Load

ext = Extract()
ld = Load()

taxa_desocupacao = ext.extract_taxa_desocupacao()
ld.insert_in_mongo(taxa_desocupacao, "desocupacao", "taxa_desocupacao")
