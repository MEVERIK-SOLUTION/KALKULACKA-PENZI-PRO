"""LangGraph agent pro penzijní dotazování.
Kombinuje pension kalkulačku + RAG knowledge + ekonomická data."""

import json
import os
import sys
from typing import Literal

# Přidání backend cest (same pattern jako api/main.py)
_BASE = os.path.join(os.path.dirname(__file__), "..", "..", "..")
sys.path.insert(0, os.path.join(_BASE, "src", "backend", "engine"))
sys.path.insert(0, os.path.join(_BASE, "src", "backend"))

from langchain_ollama import ChatOllama
from langchain_ollama import OllamaEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.tools import tool
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import END, StateGraph, MessagesState
from langgraph.prebuilt import ToolNode

from data_service import PensionDataService
from pension_calculator import calculate_pension, calculate_early_retirement
from ovz_calculator import calculate_ovz

OLLAMA_URL = os.environ.get("OLLAMA_URL", "http://localhost:11434")
MODEL = os.environ.get("AGENT_MODEL", "llama3.1")
CHROMA_URL = os.environ.get("CHROMA_URL", "http://localhost:8001")
COLLECTION_NAME = "pension_knowledge"

_llm: ChatOllama | None = None
_vector_store: Chroma | None = None


def get_llm() -> ChatOllama:
    global _llm
    if _llm is None:
        _llm = ChatOllama(model=MODEL, base_url=OLLAMA_URL, temperature=0.1)
    return _llm


def get_vector_store() -> Chroma | None:
    global _vector_store
    if _vector_store is None:
        try:
            from chromadb import HttpClient as _ChromaClient
            embeddings = OllamaEmbeddings(model=MODEL, base_url=OLLAMA_URL)
            client = _ChromaClient(host="localhost", port=8001)
            _vector_store = Chroma(
                collection_name=COLLECTION_NAME,
                embedding_function=embeddings,
                client=client,
            )
        except Exception:
            return None
    return _vector_store


@tool
def calculate_pension_tool(
    annual_income: float,
    insurance_years: int,
    excluded_days: int = 0,
) -> str:
    """Vypočítá výši starobního důchodu na základě příjmu a let pojištění."""
    result = calculate_pension(
        annual_incomes=[annual_income],
        coefficients=[1.0581],
        insurance_years=insurance_years,
        excluded_days=excluded_days,
    )
    return json.dumps(result, ensure_ascii=False)


@tool
def calculate_early_retirement_tool(
    pension_amount: float,
    months_before: int,
) -> str:
    """Vypočítá krácení důchodu při předčasném odchodu."""
    result = calculate_early_retirement(
        pension_amount=pension_amount,
        months_before=months_before,
    )
    return json.dumps(result, ensure_ascii=False)


@tool
def calculate_ovz_tool(
    annual_incomes: list[float],
    coefficients: list[float],
    total_days: int,
    excluded_days: int = 0,
) -> str:
    """Vypočítá osobní vyměřovací základ (OVZ)."""
    result = calculate_ovz(
        annual_incomes=annual_incomes,
        coefficients=coefficients,
        total_days=total_days,
        excluded_days=excluded_days,
    )
    return json.dumps({"ovz": result}, ensure_ascii=False)


@tool
def get_economic_data() -> str:
    """Získá aktuální ekonomické ukazatele (inflace, průměrná mzda, růst mezd)."""
    svc = PensionDataService()
    inflation = svc.get_latest_inflation_yoy()
    wage = svc.get_latest_avg_wage()
    growth = svc.get_wage_growth_rate(10)
    return json.dumps({
        "inflation_rate": inflation,
        "avg_wage": wage,
        "wage_growth_10y": round(growth, 2) if growth else None,
    }, ensure_ascii=False)


@tool
def query_knowledge(question: str) -> str:
    """Dotáže se znalostní báze na informace o důchodovém systému ČR."""
    store = get_vector_store()
    if store is None:
        return "Znalostní báze není dostupná."
    docs = store.similarity_search(question, k=3)
    if not docs:
        return "Žádné relevantní informace nenalezeny."
    return "\n\n".join(d.page_content for d in docs)


tools = [
    calculate_pension_tool,
    calculate_early_retirement_tool,
    calculate_ovz_tool,
    get_economic_data,
    query_knowledge,
]

SYSTEM_PROMPT = """Jsi užitečný AI asistent specializovaný na český důchodový systém.
Máš k dispozici nástroje pro výpočet důchodů, ekonomická data a znalostní bázi.

Pravidla:
1. Na základě dotazu uživatele použij relevantní nástroje
2. Pokud uživatel zadá měsíční příjem, vynásob ho 12 pro roční hodnotu
3. Výsledky vždy prezentuj v Kč a srozumitelně
4. Pokud nemáš dostatek informací, zeptej se na doplňující údaje
5. Odpovídej v češtině
6. Neodpovídej na otázky nesouvisející s důchody
"""


def should_continue(state: MessagesState) -> Literal["tools", END]:
    messages = state["messages"]
    last = messages[-1]
    if hasattr(last, "tool_calls") and last.tool_calls:
        return "tools"
    return END


def call_model(state: MessagesState):
    llm = get_llm()
    bound = llm.bind_tools(tools)
    response = bound.invoke(state["messages"])
    return {"messages": [response]}


tool_node = ToolNode(tools)

workflow = StateGraph(MessagesState)
workflow.add_node("agent", call_model)
workflow.add_node("tools", tool_node)
workflow.set_entry_point("agent")
workflow.add_conditional_edges("agent", should_continue)
workflow.add_edge("tools", "agent")

memory = MemorySaver()
agent = workflow.compile(checkpointer=memory)


async def ask_agent(question: str, thread_id: str = "default") -> str:
    """Pošle dotaz agentovi a vrátí text odpovědi."""
    system = SystemMessage(content=SYSTEM_PROMPT)
    human = HumanMessage(content=question)

    config = {"configurable": {"thread_id": thread_id}}
    result = await agent.ainvoke(
        {"messages": [system, human]},
        config=config,
    )
    messages = result["messages"]
    return messages[-1].content
