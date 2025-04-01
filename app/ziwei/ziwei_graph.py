from typing import Generator

from langchain_core.messages import HumanMessage
from langgraph.graph import StateGraph, START, END

from app.ziwei.ziwei_state import ZiweiState
from app.ziwei.ziwei_node import (
    extract_input,
    handle_error,
    generate_image,
    analyze_menh,
    analyze_phu_mau,
    analyze_phuc_duc,
    analyze_dien_trach,
    analyze_quan_loc,
    analyze_no_boc,
    analyze_thien_di,
    analyze_tat_ach,
    analyze_tai_bach,
    analyze_tu_tuc,
    analyze_phu_the,
    analyze_huynh_de,
    summarize_positive,
    summarize_negative,
    summarize_advice,
)

analyze_nodes = [
    ("analyze_menh", analyze_menh),
    ("analyze_phu_mau", analyze_phu_mau),
    ("analyze_phuc_duc", analyze_phuc_duc),
    ("analyze_dien_trach", analyze_dien_trach),
    ("analyze_quan_loc", analyze_quan_loc),
    ("analyze_no_boc", analyze_no_boc),
    ("analyze_thien_di", analyze_thien_di),
    ("analyze_tat_ach", analyze_tat_ach),
    ("analyze_tai_bach", analyze_tai_bach),
    ("analyze_tu_tuc", analyze_tu_tuc),
    ("analyze_phu_the", analyze_phu_the),
    ("analyze_huynh_de", analyze_huynh_de),
]
summarize_nodes = [
    ("summarize_positive", summarize_positive),
    ("summarize_negative", summarize_negative),
    ("summarize_advice", summarize_advice),
]


def extract_input_validation(state: ZiweiState) -> str:
    """Route to handle_error if input has error, otherwise to generate_image"""
    return state["birthchart_input"].error


workflow = StateGraph(ZiweiState)

workflow.add_node("extract_input", extract_input)
workflow.add_node("handle_error", handle_error)
workflow.add_node("generate_image", generate_image)
for node_id, node in analyze_nodes:
    workflow.add_node(node_id, node)
for node_id, node in summarize_nodes:
    workflow.add_node(node_id, node)


workflow.add_edge(START, "extract_input")
workflow.add_conditional_edges(
    "extract_input",
    extract_input_validation,
    {True: "handle_error", False: "generate_image"},
)
workflow.add_edge("handle_error", END)
for node_id, _ in analyze_nodes:
    workflow.add_edge("generate_image", node_id)
    for summarize_node_id, _ in summarize_nodes:
        workflow.add_edge(node_id, summarize_node_id)
for node_id, _ in summarize_nodes:
    workflow.add_edge(node_id, END)

graph = workflow.compile()


def run_ziwei_graph(question: str) -> Generator[tuple[str, ZiweiState], None, None]:
    initial_state = ZiweiState(messages=[HumanMessage(content=question)])
    state: dict[str, ZiweiState]
    for state in graph.stream(initial_state):
        for node_id, state_value in state.items():
            yield (node_id, state_value)
