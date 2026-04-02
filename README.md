# Pipeline ETL: Universidades e Meios de Pagamento

Este projeto é um pipeline **ETL (Extract, Transform, Load)** desenvolvido em Python. O objetivo principal é consumir dados de diferentes APIs públicas e carregá-los em diferentes tecnologias de banco de dados (SQLite e MongoDB).

## 🎯 Funcionalidades

- **Extração (Extract):**
  - Dados de universidades ao redor do mundo a partir do país (utilizando a API pública do [HipoLabs](http://universities.hipolabs.com/)).
  - Dados sobre os meios de pagamento trimestrais no Brasil (utilizando a API de Dados Abertos do **Banco Central do Brasil**).
- **Carregamento (Load):**
  - Carga de dados tabulares em banco de dados relacional local usando **SQLite**.
  - Carga de dados (JSON/documentos) em banco de dados NoSQL na nuvem utilizando **MongoDB Atlas**.

## 📂 Estrutura do Projeto

```
etl-uni/
│
├── main.py               # Script principal que orquestra o fluxo ETL
├── teste.py              # Script local para testes de requisição da API
├── .env                  # Variáveis de ambiente com credenciais (não versionado)
│
└── src/
    ├── extract.py        # Módulo contendo as funções de extração (requests)
    └── load.py           # Módulo contendo as funções de carga de banco de dados
```

## 🚀 Como Executar

### 1. Pré-requisitos
- Python 3.10 ou superior
- O gerenciador de pacotes `pip`
- Uma conta no MongoDB Atlas com um cluster (ex: `Cluster0`) e permissões configuradas.

### 2. Instalação e Configuração

Crie um ambiente virtual (recomendado) e instale as dependências:
```bash
python -m venv .venv
source .venv/bin/activate  # ou .venv\Scripts\activate no Windows
pip install -r requirements.txt
```

Crie um arquivo `.env` na raiz do seu projeto e adicione as suas credenciais do MongoDB:
```env
DB_USER=seu_usuario_do_mongo
DB_PASSWORD=sua_senha_do_mongo
```

### 3. Rodando o Pipeline

Basta executar o arquivo principal:
```bash
python main.py
```