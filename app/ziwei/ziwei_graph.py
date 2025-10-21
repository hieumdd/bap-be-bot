from langchain_core.messages import HumanMessage
from langgraph.graph import StateGraph, START, END

from app.core.chat_model import ChatModelService
from app.ziwei.ziwei_state import ZiweiTellingState
from app.ziwei.ziwei_node import (
    ExtractZiweiBirthchart,
    MapAnalyzeZiweiArcs,
    ValidateZiweiBirthchart,
    HandleZiweiBirthchartError,
    DumpZiweiBirthchartImage,
    AnalyzeZiweiArc,
    DumpZiweiArcAnalysis,
    MapSummarizeZiwei,
    SummarizeZiwei,
)


class ZiweiGraphService:
    def __init__(self, chat_model_service: ChatModelService):
        workflow = StateGraph(ZiweiTellingState)

        workflow.add_node(ExtractZiweiBirthchart.__name__, ExtractZiweiBirthchart(chat_model_service))
        workflow.add_node(HandleZiweiBirthchartError.__name__, HandleZiweiBirthchartError())
        workflow.add_node(DumpZiweiBirthchartImage.__name__, DumpZiweiBirthchartImage())
        workflow.add_node(AnalyzeZiweiArc.__name__, AnalyzeZiweiArc(chat_model_service))
        workflow.add_node(DumpZiweiArcAnalysis.__name__, DumpZiweiArcAnalysis())
        workflow.add_node(SummarizeZiwei.__name__, SummarizeZiwei(chat_model_service))

        workflow.add_edge(START, ExtractZiweiBirthchart.__name__)

        workflow.add_conditional_edges(
            ExtractZiweiBirthchart.__name__,
            ValidateZiweiBirthchart(),
            {True: HandleZiweiBirthchartError.__name__, False: DumpZiweiBirthchartImage.__name__},
        )
        workflow.add_edge(HandleZiweiBirthchartError.__name__, END)

        workflow.add_conditional_edges(
            DumpZiweiBirthchartImage.__name__,
            MapAnalyzeZiweiArcs(AnalyzeZiweiArc.__name__),
            [AnalyzeZiweiArc.__name__],
        )
        workflow.add_edge(AnalyzeZiweiArc.__name__, DumpZiweiArcAnalysis.__name__)
        workflow.add_conditional_edges(
            DumpZiweiArcAnalysis.__name__,
            MapSummarizeZiwei(SummarizeZiwei.__name__),
            [SummarizeZiwei.__name__],
        )
        workflow.add_edge(SummarizeZiwei.__name__, END)

        self.graph = workflow.compile()

    def run(self, question: str):
        initial_state = ZiweiTellingState(messages=[HumanMessage(content=question)])
        state: dict[str, ZiweiTellingState]
        for state in self.graph.stream(initial_state):
            for node_id, state_value in state.items():
                yield (node_id, state_value)
