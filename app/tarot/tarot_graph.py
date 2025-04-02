from typing import Generator

from langchain_core.messages import HumanMessage
from langgraph.types import Send
from langgraph.graph import StateGraph, START, END

from app.tarot.tarot_state import TarotState
from app.tarot.tarot_node import randomize_tarot_cards, analyze_card


def map_analyze_card(state: TarotState):
    return [
        Send(
            "analyze_card",
            {"question": state["messages"][0].content, "tarot_telling_card": ttc},
        )
        for ttc in state["tarot_telling_cards"]
    ]


workflow = StateGraph(TarotState)

workflow.add_node("randomize_tarot_cards", randomize_tarot_cards)
workflow.add_node("analyze_card", analyze_card)


workflow.add_edge(START, "randomize_tarot_cards")
workflow.add_conditional_edges(
    "randomize_tarot_cards",
    map_analyze_card,
    ["analyze_card"],
)
workflow.add_edge("analyze_card", END)

graph = workflow.compile()


def run_tarot_graph(question: str) -> Generator[tuple[str, TarotState], None, None]:
    initial_state = TarotState(messages=[HumanMessage(content=question)])
    state: dict[str, TarotState]
    for state in graph.stream(initial_state):
        for node_id, state_value in state.items():
            yield (node_id, state_value)
