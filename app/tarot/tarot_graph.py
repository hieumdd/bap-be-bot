from langchain_core.messages import HumanMessage
from langgraph.graph import StateGraph, START, END

from app.core.chat_model import ChatModelService
from app.tarot.tarot_state import TarotTellingState
from app.tarot.tarot_node import RandomizeTarotCards, MapAnalyzeTarotCards, AnalyzeTarotCard, SummarizeTarotCards


class TarotGraphService:
    def __init__(self, chat_model_service: ChatModelService):
        workflow = StateGraph(TarotTellingState)

        workflow.add_node(RandomizeTarotCards.__name__, RandomizeTarotCards())
        workflow.add_node(AnalyzeTarotCard.__name__, AnalyzeTarotCard(chat_model_service))
        workflow.add_node(SummarizeTarotCards.__name__, SummarizeTarotCards(chat_model_service))

        workflow.add_edge(START, RandomizeTarotCards.__name__)
        workflow.add_conditional_edges(
            RandomizeTarotCards.__name__,
            MapAnalyzeTarotCards(AnalyzeTarotCard.__name__),
            [AnalyzeTarotCard.__name__],
        )
        workflow.add_edge(AnalyzeTarotCard.__name__, SummarizeTarotCards.__name__)
        workflow.add_edge(SummarizeTarotCards.__name__, END)

        self.graph = workflow.compile()

    def run(self, question: str):
        initial_state = TarotTellingState(messages=[HumanMessage(content=question)])
        state: dict[str, TarotTellingState]
        for state in self.graph.stream(initial_state):
            for node_id, state_value in state.items():
                yield (node_id, state_value)
