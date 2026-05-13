# Pipeline ETL: IBGE Desocupação

Este projeto é um pipeline **ETL (Extract, Transform, Load)** desenvolvido em Python com **Prefect** para orquestração. O objetivo é extrair dados de taxa de desocupação do **IBGE** e carregar em **MongoDB Atlas**.

## 🎯 Funcionalidades

- **Extração (Extract):**
  - Dados de taxa de desocupação do IBGE.
- **Carregamento (Load):**
  - Carga de dados em banco de dados NoSQL usando **MongoDB Atlas**.
- **Orquestração:**
  - Prefect para executar o pipeline e registrar logs.

## 📂 Estrutura do Projeto

```
etl-ibge-desocupacao/
│
├── orchestrate.py        # Script principal com o flow Prefect
├── main.py               # Script auxiliar para testar a extração e carga
├── .env.example          # Exemplo de variáveis de ambiente
│
└── src/
    ├── extract.py        # Módulo com a extração dos dados do IBGE
    ├── load.py           # Módulo com a carga no MongoDB
    └── __init__.py       # Inicializador do pacote
```

## 🚀 Como Executar

### 1. Pré-requisitos
- Python 3.12 ou superior
- O gerenciador de pacotes `pip`
- Uma conta no MongoDB Atlas com a URI de conexão.

### 2. Instalação e Configuração

Crie um ambiente virtual e instale as dependências:
```bash
python -m venv .venv
source .venv/bin/activate  # ou .venv\Scripts\activate no Windows
pip install -r requirements.txt
```

Crie um arquivo `.env` na raiz do projeto com a URI do MongoDB Atlas:
```env
MONGO_URI=sua_uri_do_mongodb_atlas
```

### 3. Iniciando o servidor Prefect

Suba o servidor de monitoramento **antes** de rodar o pipeline:
```bash
prefect server start
```

Deixe esse terminal aberto e acesse `http://127.0.0.1:4200` para ver o dashboard.

### 4. Rodando o Pipeline

Em **outro terminal** (com o `.venv` ativado), execute o flow:
```bash
python orchestrate.py
```

O run vai aparecer no dashboard em tempo real com logs e status de cada task.
