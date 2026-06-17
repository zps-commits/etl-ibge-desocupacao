import requests
from datetime import datetime


class Extract:
    def __init__(self, periodo=None, localidade="N3[26]", variaveis="4099|4096|12466"):
        if periodo is None:
            agora = datetime.now()
            tri = (agora.month - 1) // 3 + 1
            periodo = f"201201-{agora.year}{tri:02d}"
        self.base_url = (
            f"https://servicodados.ibge.gov.br/api/v3/agregados/4093"
            f"/periodos/{periodo}/variaveis/{variaveis}"
        )
        self.localidade = localidade

    def extract_indicadores(self):
        """Retorna JSON cru da API do IBGE. Tenta até 3 vezes em caso de falha."""
        parametros = {
            "localidades": self.localidade,
            "classificacao": "2[6794,4,5]",
        }

        for tentativa in range(1, 4):
            try:
                response = requests.get(self.base_url, params=parametros, timeout=30)
                response.raise_for_status()
                return response.json()
            except Exception as e:
                if tentativa == 3:
                    raise
                print(f"Tentativa {tentativa} falhou: {e}. Tentando novamente...")
