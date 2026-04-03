import requests


class Extract:
    def __init__(self):
        pass

    def extract_country(self, country):
        url = f"http://universities.hipolabs.com/search?country={country}"
        response = requests.get(url)
        return response.json()

    def extract_meios_pagamentos(self, trimestre: str, n_retornos: str):
        url = (
            "https://olinda.bcb.gov.br/olinda/servico/MPV_DadosAbertos/versao/v1/odata/"
            f"MeiosdePagamentosTrimestralDA(trimestre=@trimestre)?@trimestre='{trimestre}'"
            f"&$top={n_retornos}&$format=json&$select=datatrimestre,valorPix,valorCartaoCredito,"
            "valorCartaoDebito,quantidadePix,quantidadeCartaoCredito,quantidadeCartaoDebito"
        )
        response = requests.get(url)
        return response.json()

    def extract_taxa_desocupacao(self):
        base_url = "https://servicodados.ibge.gov.br/api/v3/agregados/4093/periodos/201201-202504/variaveis/4099"

        parametros = {
            "localidades": "N3[26]",
            "classificacao": "2[6794,4,5]"
        }

        response = requests.get(base_url, params=parametros)
        data = response.json()
        documentos = []

        resultados = data[0]["resultados"]

        for resultado in resultados:
            categoria = list(resultado["classificacoes"][0]["categoria"].values())[0]
            serie = resultado["series"][0]["serie"]

        for periodo, valor in serie.items():
            # ignora valores ausentes
            if valor == "..." or valor is None or valor == "":
                continue

            documentos.append({
                "localidade": "Pernambuco",
                "categoria": categoria,
                "periodo": periodo,
                "taxa_desocupacao": float(str(valor).replace(",", "."))
            })

        return documentos
