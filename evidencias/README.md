# Evidências do Projeto ETL IBGE

Esta pasta guarda capturas que comprovam o funcionamento completo do pipeline.

---

## O que capturar

### 1. Execução do ETL direto (`log_etl.txt`)

Rode o pipeline e salve o log:

```bash
python main.py 2>&1 | tee evidencias/log_etl.txt
```

O log deve mostrar as 3 etapas, o total de registros extraídos e a confirmação do upsert no MongoDB:

```
[1/3] Extraindo dados da API do IBGE...
[2/3] Transformando dados...
Total de registros: 177
[3/3] Carregando dados no MongoDB Atlas...
Conectado ao MongoDB Atlas com sucesso!
Inseridos: 177
Atualizados: 0
```

---

### 2. Painel do Prefect (`prefect_run.png`)

1. Suba o servidor: `prefect server start`
2. Execute o flow: `python orchestrate.py`
3. Acesse `http://127.0.0.1:4200` e tire print do run verde com as 3 tasks (extract → transform → load).

---

### 3. Deployment agendado (`prefect_deployment.png`)

Registre o deployment trimestral:

```bash
python orchestrate.py --deploy
```

Tire print da tela de **Deployments** no painel do Prefect mostrando o agendamento `0 6 1 1,4,7,10 *`.

---

### 4. Documentos no MongoDB Atlas (`mongodb_docs.png`)

No Atlas UI, abra `desocupacao > taxa_desocupacao` e tire print dos documentos,
mostrando os campos `indicador`, `categoria`, `periodo`, `localidade` e `valor`.

---

### 5. Consulta em linguagem natural (`app_resposta.png`)

Suba o Streamlit:

```bash
streamlit run app.py
```

Faça a pergunta:
> "Qual a taxa de desocupação das mulheres em Pernambuco no último trimestre disponível?"

Tire print da resposta gerada pelo modelo, citando o período e o valor em %.

---

## Arquivos esperados nesta pasta

| Arquivo              | Descrição                                    |
|----------------------|----------------------------------------------|
| `log_etl.txt`        | Log completo da execução de `main.py`        |
| `prefect_run.png`    | Run verde no painel Prefect com 3 tasks      |
| `prefect_deploy.png` | Deployment trimestral registrado             |
| `mongodb_docs.png`   | Documentos na coleção do Atlas               |
| `app_resposta.png`   | Consulta em linguagem natural via Streamlit  |
