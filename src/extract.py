import requests


class Extract:
    def __init__(self):
        pass

    def extract_taxa_desocupacao(self):
        base_url = "https://servicodados.ibge.gov.br/api/v3/agregados/4093/periodos/201201-202504/variaveis/4099"

        parametros = {
            "localidades": "N3[26]",
            "classificacao": "2[6794,4,5]"
        }

        response = requests.get(base_url, params=parametros)
        response.raise_for_status()
        data = response.json()
        documentos = []

        resultados = data[0]["resultados"]

        for resultado in resultados:
            categoria = list(resultado["classificacoes"][0]["categoria"].values())[0]
            serie = resultado["series"][0]["serie"]

            for periodo, valor in serie.items():
                if valor in ["...", None, ""]:
                    continue

                documentos.append({
                    "localidade": "Pernambuco",
                    "categoria": categoria,
                    "periodo": periodo,
                    "taxa_desocupacao": float(str(valor).replace(",", "."))
                })

        return documentos
