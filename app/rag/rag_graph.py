from typing import Generator

from langchain.schema import HumanMessage
from langgraph.graph import StateGraph, START, END

from app.rag.rag_state import RagState
from app.rag.rag_node import rag

workflow = StateGraph(RagState)

workflow.add_node("rag", rag)

workflow.add_edge(START, "rag")
workflow.add_edge("rag", END)

graph = workflow.compile()


def run_rag_graph(question: str) -> Generator[tuple[str, RagState], None, None]:
    initial_state = RagState(messages=[HumanMessage(content=question)])
    state: dict[str, RagState]
    for state in graph.stream(initial_state):
        for node_id, state_value in state.items():
            yield (node_id, state_value)
