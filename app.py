import json
import os
import asyncio
import streamlit as st
from openai import OpenAI
from fastmcp import Client
from mcp_server import mcp
from dotenv import load_dotenv

load_dotenv()

openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def run_async(coro):
    """Executa corrotina em thread separada para não conflitar com o event loop do Streamlit."""
    with __import__("concurrent.futures", fromlist=["ThreadPoolExecutor"]).ThreadPoolExecutor() as pool:
        return pool.submit(asyncio.run, coro).result()


async def _list_tools():
    async with Client(mcp) as client:
        return await client.list_tools()


async def _call_tool(name: str, args: dict):
    async with Client(mcp) as client:
        return await client.call_tool(name, args)


def to_openai_tool(t) -> dict:
    return {
        "type": "function",
        "function": {
            "name": t.name,
            "description": t.description or "",
            "parameters": t.inputSchema,
        },
    }


SYSTEM_PROMPT = """Você é um analista de mercado de trabalho especializado nos dados da PNAD Contínua Trimestral do IBGE para Pernambuco.

## Uso da tool
- Use a tool `buscar_indicadores_pnad` para consultar os dados.
- Formato do período: YYYYT (ex: '20251' = 1º trim 2025, '20244' = 4º trim 2024).
- Use periodo='ultimo' quando o usuário pedir o dado mais recente ou atual.
- Indicadores disponíveis: 'taxa_desocupacao', 'taxa_participacao', 'taxa_informalidade'.
- Categorias disponíveis: 'Total', 'Homens', 'Mulheres'.

## Dados retornados
Os valores já estão em percentual (%):
- taxa_desocupacao   → % de pessoas desocupadas na força de trabalho
- taxa_participacao  → % da população de 14+ que está na força de trabalho
- taxa_informalidade → % de ocupados em situação informal

## Formatação das respostas
- Sempre cite o período (trimestre e ano) do dado retornado.
- Apresente o valor com uma casa decimal seguido de %.
- Compare com períodos anteriores quando relevante.
- Responda sempre em português, de forma clara e objetiva.

## Exemplos de perguntas
- Qual a taxa de desocupação das mulheres em Pernambuco no último trimestre?
- Como está a informalidade em 2024?
- Compare a participação de homens e mulheres na força de trabalho.
"""


def chat(pergunta: str) -> str:
    mcp_tools = run_async(_list_tools())
    openai_tools = [to_openai_tool(t) for t in mcp_tools]

    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": pergunta},
    ]

    response = openai_client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages,
        tools=openai_tools,
    )

    msg = response.choices[0].message
    messages.append(msg)

    if msg.tool_calls:
        for tc in msg.tool_calls:
            resultado = run_async(_call_tool(tc.function.name, json.loads(tc.function.arguments)))
            content = resultado.content[0].text if resultado and resultado.content else "sem resultado"
            messages.append({
                "role": "tool",
                "tool_call_id": tc.id,
                "content": content,
            })

        final = openai_client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages,
        )
        return final.choices[0].message.content

    return msg.content


st.title("Indicadores de Emprego — IBGE Pernambuco")
st.caption("Dados da PNAD Contínua Trimestral | Taxa de desocupação, participação e informalidade")

pergunta = st.text_input(
    "Pergunta",
    placeholder="Ex: Qual a taxa de desocupação das mulheres no último trimestre?"
)

if st.button("Enviar") and pergunta:
    with st.spinner("Consultando..."):
        resposta = chat(pergunta)
    st.write(resposta)
