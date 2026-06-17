# ETL — Indicadores de Emprego IBGE (PNAD Contínua)

Pipeline de Engenharia de Dados para coleta, tratamento, armazenamento, orquestração e consulta de indicadores de emprego do IBGE, com servidor MCP para consultas em linguagem natural.

---

## Objetivo

Coletar e disponibilizar os seguintes indicadores da PNAD Contínua Trimestral para Pernambuco, organizados por variável, sexo e período:

- **Taxa de desocupação** — percentual de pessoas desocupadas na força de trabalho
- **Taxa de participação na força de trabalho** — percentual da população de 14+ na força de trabalho
- **Taxa de informalidade** — percentual de ocupados em situação informal

---

## Fonte dos Dados

- **API:** IBGE — Agregados v3
- **Tabela:** 4093 — PNAD Contínua Trimestral
- **Variáveis:** 4099 (desocupação), 4096 (participação), 12466 (informalidade)
- **Localidade:** Pernambuco (código N3[26])
- **Classificação:** por sexo — Total (6794), Homens (4), Mulheres (5)
- **Período:** 2012T1 até o trimestre mais recente disponível

---

## Arquitetura da Solução

```
API IBGE (v3)
     │
     ▼
src/extract.py       ← classe Extract — consome a API, devolve JSON cru
     │
     ▼
src/transform.py     ← classe Transform — normaliza dados, trata ausentes, adiciona data_coleta
     │
     ▼
src/load.py          ← classe Load — grava no MongoDB com upsert
     │
     ▼
MongoDB Atlas        ← banco de dados em nuvem
     │
     ▼
mcp_server.py        ← servidor MCP — expõe tool para consultas via IA
     │
     ▼
app.py               ← interface Streamlit com GPT-4o-mini via MCP
```

**Orquestração:** `orchestrate.py` — Prefect gerencia o fluxo com 3 tasks, retries e agendamento trimestral.

---

## Estrutura do Projeto

```
etl-ibge-desocupacao/
├── src/
│   ├── extract.py        # Extração da API do IBGE (JSON cru)
│   ├── transform.py      # Normalização e tratamento dos dados
│   ├── load.py           # Carga no MongoDB Atlas com upsert
│   └── __init__.py
├── evidencias/
│   └── README.md         # O que capturar como evidência de funcionamento
├── main.py               # Execução direta do ETL (3 etapas)
├── orchestrate.py        # Flow Prefect com tasks, retries e deployment
├── mcp_server.py         # Servidor MCP para consultas via IA
├── app.py                # Interface Streamlit + GPT-4o-mini + MCP
├── requirements.txt
├── .env.example
└── README.md
```

---

## Instalação

**Pré-requisitos:** Python 3.12+, conta no MongoDB Atlas, chave de API da OpenAI.

```bash
# 1. Criar ambiente virtual
python3.12 -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

# 2. Instalar dependências
pip install -r requirements.txt

# 3. Configurar variáveis de ambiente
cp .env.example .env
# Editar .env e preencher MONGO_URI e OPENAI_API_KEY
```

### Variáveis de ambiente

| Variável        | Descrição                                            |
|-----------------|------------------------------------------------------|
| `MONGO_URI`     | URI de conexão do MongoDB Atlas                      |
| `OPENAI_API_KEY`| Chave da API OpenAI (usada pelo app.py / Streamlit)  |

---

## Como Executar

### 1. ETL direto

```bash
python main.py
```

Executa as 3 etapas em sequência: extrai da API → transforma → grava no MongoDB.

### 2. ETL com Prefect

**Terminal 1 — subir o painel:**
```bash
prefect server start
```

Deixe esse terminal aberto e acesse `http://127.0.0.1:4200` para ver o dashboard.

**Terminal 2 — executar o flow:**
```bash
python orchestrate.py
```

O run aparece no dashboard em tempo real com logs e status de cada task.

### 3. Deployment trimestral (agendamento automático)

Para registrar o deployment com cron trimestral (dia 1 de jan, abr, jul e out às 06:00 UTC):

```bash
# Com o servidor Prefect rodando em outro terminal:
python orchestrate.py --deploy
```

O deployment fica visível no painel em `http://127.0.0.1:4200/deployments`.

### 4. Servidor MCP

```bash
python mcp_server.py
```

Expõe a tool `buscar_indicadores_pnad` para clientes de IA via protocolo MCP.

### 5. Interface Streamlit

```bash
streamlit run app.py
```

Abre uma interface web onde você pergunta em linguagem natural e o GPT-4o-mini consulta o MongoDB via MCP.

**Exemplo de pergunta:**
> "Qual a taxa de desocupação das mulheres em Pernambuco no último trimestre disponível?"

---

## Modelagem no MongoDB

**Banco:** `desocupacao`
**Coleção:** `taxa_desocupacao`

### Estrutura do documento

```json
{
  "indicador":   "taxa_desocupacao",
  "localidade":  "Pernambuco",
  "categoria":   "Mulheres",
  "periodo":     "202601",
  "ano":         2026,
  "trimestre":   1,
  "valor":       9.7,
  "unidade":     "%",
  "fonte":       "IBGE - PNAD Contínua Trimestral",
  "data_coleta": "2026-06-17T10:00:00+00:00"
}
```

### Justificativa

- **Granularidade:** um documento por indicador + sexo + período + localidade
- **Chave de upsert:** `indicador + categoria + periodo + localidade` — garante idempotência em reexecuções
- **Índice único:** `idx_indicador_categoria_periodo_localidade` — impede duplicidade no banco
- **Metadados:** `fonte`, `data_coleta` e `unidade` garantem rastreabilidade

---

## Servidor MCP

O servidor expõe a tool `buscar_indicadores_pnad` com os seguintes filtros:

| Parâmetro   | Descrição                                                    | Exemplo              |
|-------------|--------------------------------------------------------------|----------------------|
| `indicador` | `taxa_desocupacao`, `taxa_participacao`, `taxa_informalidade` | `"taxa_desocupacao"` |
| `localidade`| UF desejada                                                  | `"Pernambuco"`       |
| `categoria` | Sexo: `Total`, `Homens` ou `Mulheres`                        | `"Mulheres"`         |
| `periodo`   | Formato YYYYT ou `"ultimo"` para o mais recente              | `"20251"` / `"ultimo"` |

---

## Evidências

Ver [evidencias/README.md](evidencias/README.md) para instruções de como gerar e salvar as capturas de tela e logs que comprovam o funcionamento do pipeline.

---

## Integrantes

- Gabriel Costa
- João Souza
- Lucas Collier
- Renan Caminha
- Thiago Alves
- Vinicius Queiroz
- Zion Silva
