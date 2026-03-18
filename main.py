from src.extract import Extract
from src.load import Load


ext = Extract()
ld = Load()

br = ext.extract_country("Brazil")
ld.create_sqlite_table(br, "universidades", "uni_br")

it = ext.extract_country("Italy")
ld.create_sqlite_table(it, "universidades", "uni_it")

