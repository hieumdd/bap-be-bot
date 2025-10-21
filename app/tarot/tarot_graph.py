from langchain_core.messages import HumanMessage
from langgraph.graph import StateGraph, START, END

from app.core.chat_model import ChatModelService
from app.tarot.tarot_state import TarotTellingState
from app.tarot.tarot_node import RandomizeTarotCards, MapTarotCards, AnalyzeTarotCard, SummarizeTarotCards


class TarotGraphService:
    def __init__(self, chat_model_service: ChatModelService):
        workflow = StateGraph(TarotTellingState)

        workflow.add_node("RandomizeTarotCards", RandomizeTarotCards())
        workflow.add_node("AnalyzeTarotCard", AnalyzeTarotCard(chat_model_service))
        workflow.add_node("SummarizeTarotCards", SummarizeTarotCards(chat_model_service))

        workflow.add_edge(START, "RandomizeTarotCards")
        workflow.add_conditional_edges("RandomizeTarotCards", MapTarotCards("AnalyzeTarotCard"), ["AnalyzeTarotCard"])
        workflow.add_edge("AnalyzeTarotCard", "SummarizeTarotCards")
        workflow.add_edge("SummarizeTarotCards", END)

        self.graph = workflow.compile()

    def run(self, question: str):
        initial_state = TarotTellingState(messages=[HumanMessage(content=question)])
        state: dict[str, TarotTellingState]
        for state in self.graph.stream(initial_state):
            for node_id, state_value in state.items():
                yield (node_id, state_value)
