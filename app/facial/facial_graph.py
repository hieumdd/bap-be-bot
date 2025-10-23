from langgraph.graph import StateGraph, START, END

from app.core.chat_model import ChatModelService
from app.facial.facial_state import FacialTellingState
from app.facial.facial_node import (
    ExtractFacialFeatures,
    ValidateFacialFeatures,
    HandleFacialFeaturesExtractionError,
    DumpFacialFeatures,
    AnalyzeFacialFeatures,
)


class FacialGraphService:
    def __init__(self, chat_model_service: ChatModelService):
        workflow = StateGraph(FacialTellingState)

        workflow.add_node(ExtractFacialFeatures.__name__, ExtractFacialFeatures(chat_model_service))
        workflow.add_node(HandleFacialFeaturesExtractionError.__name__, HandleFacialFeaturesExtractionError())
        workflow.add_node(DumpFacialFeatures.__name__, DumpFacialFeatures())
        workflow.add_node(AnalyzeFacialFeatures.__name__, AnalyzeFacialFeatures(chat_model_service))

        workflow.add_edge(START, ExtractFacialFeatures.__name__)

        workflow.add_conditional_edges(
            ExtractFacialFeatures.__name__,
            ValidateFacialFeatures(),
            {True: HandleFacialFeaturesExtractionError.__name__, False: DumpFacialFeatures.__name__},
        )
        workflow.add_edge(HandleFacialFeaturesExtractionError.__name__, END)
        workflow.add_edge(DumpFacialFeatures.__name__, AnalyzeFacialFeatures.__name__)
        workflow.add_edge(AnalyzeFacialFeatures.__name__, END)

        self.graph = workflow.compile()

    def run(self, image_url: str):
        initial_state = FacialTellingState(image_url=image_url)
        state: dict[str, FacialTellingState]
        for state in self.graph.stream(initial_state):
            for node_id, state_value in state.items():
                yield (node_id, state_value)
