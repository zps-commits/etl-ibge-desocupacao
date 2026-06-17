from datetime import datetime, timezone

VARIAVEIS = {
    "4099": "taxa_desocupacao",
    "4096": "taxa_participacao",
    "12466": "taxa_informalidade",
}


class Transform:
    def transform(self, dados_brutos, localidade_nome="Pernambuco"):
        """Normaliza JSON cru da API e devolve lista de documentos prontos para o MongoDB."""
        documentos = []
        data_coleta = datetime.now(timezone.utc).isoformat()

        for variavel in dados_brutos:
            indicador = VARIAVEIS.get(variavel["id"])
            if not indicador:
                continue

            for resultado in variavel["resultados"]:
                categoria = list(resultado["classificacoes"][0]["categoria"].values())[0]
                serie = resultado["series"][0]["serie"]

                for periodo, valor in serie.items():
                    # "-" e "..." são valores ausentes na API do IBGE
                    if valor in ("...", "-", None, ""):
                        continue

                    ano = int(periodo[:4])
                    trimestre = int(periodo[4:])

                    documentos.append({
                        "localidade": localidade_nome,
                        "indicador": indicador,
                        "categoria": categoria,
                        "periodo": periodo,
                        "ano": ano,
                        "trimestre": trimestre,
                        "valor": float(str(valor).replace(",", ".")),
                        "unidade": "%",
                        "fonte": "IBGE - PNAD Contínua Trimestral",
                        "data_coleta": data_coleta,
                    })

        return documentos
